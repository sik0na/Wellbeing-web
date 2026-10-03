# app.py - the backend: a Flask REST API (/api/...) that also serves the built React app.
#
# Run on your laptop:   python app.py          (http://127.0.0.1:5002)
# Run on a server:      gunicorn app:app       (see Dockerfile)

import os
import calendar
from flask import Flask, request, session, jsonify, send_from_directory
import joblib
from sentence_transformers import SentenceTransformer
import content
import database
import translations

# The folder of this file, so files are found from any folder (also in tests/)
HERE = os.path.dirname(os.path.abspath(__file__))
# Where "npm run build" puts the finished React app
REACT_FOLDER = os.path.join(HERE, "frontend", "dist")

# device="cpu": servers have no graphics card, and on a Mac the graphics chip crashes inside gunicorn
encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device="cpu")
classifier = joblib.load(os.path.join(HERE, "emotion_model_multi.joblib"))

def predict_emotion(text):
    numbers = encoder.encode([text], normalize_embeddings=True)
    return str(classifier.predict(numbers)[0])

database.create_tables()

# static_folder=None: we serve the React files ourselves (see react_app at the bottom)
app = Flask(__name__, static_folder=None)
# The secret key signs the login cookie. On the server it comes from an environment
# variable, so the real key is never on GitHub.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")


@app.route("/api/history")
def api_history():
    if "user_id" not in session:
          return jsonify({"error": "Please log in."}), 401

    checkins= []

    for row in database.get_all_checkins(session["user_id"]):
        checkins.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "text": row["text"],
            "chosen": row["chosen"],
        })
    return jsonify({"checkins": checkins})


@app.route("/api/checkin", methods=["Post"])
def api_checkin():
    if "user_id" not in session:
        return jsonify({"error": "Please log in."}), 401
    data = request.get_json()
    text = data["text"]
    lang = data.get("lang", "en")
    emotion = predict_emotion(text)
    return jsonify({
        "emotion": emotion,
        "name": translations.translate(content.EMOTIONS[emotion]["name"], lang),
        "emoji": content.EMOTIONS[emotion]["emoji"],
    })

@app.route("/api/message", methods=["post"]) 
def api_message():
    if "user_id" not in session:
        return jsonify({"error": "Please log in."}), 401
    data = request.get_json()
    chosen = data["chosen"]
    lang = data.get("lang", "en")
    return jsonify({"message": translations.translate(content.EMOTIONS[chosen]["message"], lang)})
    

@app.route("/api/save", methods=["post"])
def api_save():
    if "user_id" not in session:
       return jsonify({"error": "Please log in."}), 401
    data = request.get_json()
    database.save_checkin(session["user_id"], data["text"], data["predicted"], data["chosen"])
    return jsonify({"ok": True})  

@app.route("/api/signup", methods=["post"])
def api_signup():
    data = request.get_json()
    username = data["username"].strip()      # " anna " -> "anna"
    password = data["password"]
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400
    user_id = database.create_user(username, password)
    if user_id is None:
        return jsonify({"error": "That username is already taken."}), 400
    session["user_id"] = user_id
    return jsonify({"username": username})

@app.route("/api/login", methods = ["Post"])
def api_login():
    data = request.get_json()
    user = database.check_login(data["username"], data["password"])
    if user is None:
        return jsonify({"error": "Wrong username or password"}), 401
    session["user_id"] = user["id"]
    return jsonify({"username": user["username"]})

@app.route("/api/logout", methods= ["post"])
def api_logout():
    session.clear() 
    return jsonify({"ok": True})

@app.route("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True})

@app.route("/api/emotions")
def api_emotions():
    if "user_id" not in session:
        return jsonify({"error": "Please log in."}), 401
    lang = request.args.get("lang", "en")   # from the address: /api/emotions?lang=hu
    emotions = []
    for key in content.EMOTIONS:
        emotions.append({
            "key": key,
            "name": translations.translate(content.EMOTIONS[key]["name"], lang),
            "emoji": content.EMOTIONS[key]["emoji"],
        })
    return jsonify({"emotions": emotions})

@app.route("/api/translations/<lang>")
def api_translations(lang):
    if lang not in translations.LANGUAGES:
        return jsonify({"error": "Language not supported."}), 404
    return jsonify({"texts": translations.TRANSLATIONS.get(lang, {})})

@app.route("/api/calendar/<int:year>/<int:month>")
def api_calendar(year, month):
    if "user_id" not in session:
        return jsonify({"error": "Please log in."}), 401
    if month < 1 or month > 12:
        return jsonify({"error": "Month must be 1-12."}), 400

    moods = {}
    for row in database.get_all_checkins(session["user_id"]):
        day = row["created_at"][:10]
        if day not in moods:
            moods[day] = row["chosen"]

    weeks = []
    for week in calendar.monthcalendar(year, month):
        days = []
        for number in week:
            if number == 0:
                days.append(None)
                continue
            date = f"{year}-{month:02d}-{number:02d}"
            emotion = moods.get(date)

            days.append({
                "number": number,
                "date": date,
                "emotion": emotion,
                "emoji": content.EMOTIONS[emotion]["emoji"] if emotion else "",
            })
        weeks.append(days)
    return jsonify({"weeks": weeks})


# ----- The React app -----
# Every address that is not /api/... gets the React app (frontend/dist).
# React then decides what to show. So only ONE server is needed.
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def react_app(path):
    if path.startswith("api/"):
        return jsonify({"error": "Not found."}), 404       # unknown API address
    if not os.path.exists(os.path.join(REACT_FOLDER, "index.html")):
        return "The React app is not built yet. Run: cd frontend && npm run build", 404
    if path and os.path.isfile(os.path.join(REACT_FOLDER, path)):
        return send_from_directory(REACT_FOLDER, path)      # a real file, e.g. assets/index-abc.js
    return send_from_directory(REACT_FOLDER, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)

