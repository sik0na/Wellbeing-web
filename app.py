from flask import Flask, render_template, request, redirect, session, jsonify
import joblib
import content
import database
from sentence_transformers import SentenceTransformer
import translations
import calendar

encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
classifier = joblib.load("emotion_model_multi.joblib")
def predict_emotion(text):
    numbers = encoder.encode([text], normalize_embeddings=True)
    return str(classifier.predict(numbers)[0])
    
database.create_tables()

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/checkin", methods = ["POST"])
def checkin():
    if "user_id" not in session:
        return redirect("/login")
    text = request.form["text"]
    emotion = predict_emotion(text)
    return render_template("result.html", text=text, emotion=emotion, emotions=content.EMOTIONS)

@app.route("/message", methods = ["POST"])
def message():
    if "user_id" not in session:
            return redirect("/login")
    chosen=request.form["chosen"]
    text = request.form["text"]
    predicted = request.form["predicted"]
    return render_template("message.html", emotion=content.EMOTIONS[chosen],
                        text = text, predicted=predicted, chosen=chosen)

@app.route("/save", methods = ["POST"])
def save():
    if "user_id" not in session:
            return redirect("/login")
    database.save_checkin(session["user_id"], request.form["text"],
                          request.form["predicted"], request.form["chosen"])
    return redirect("/history")


@app.route("/history")
def history():
    if "user_id" not in session:
            return redirect("/login")
    return render_template("history.html",
                           checkins=database.get_all_checkins(session["user_id"]), emotions=content.EMOTIONS)


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = database.create_user(request.form["username"], request.form["password"])
        if user_id is None:
            return render_template("signup.html", error="That username is already takem.")
        session["user_id"] = user_id
        return redirect("/")
    return render_template("signup.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user = database.check_login(request.form["username"], request.form["password"])
        if user is None:
            return render_template("login.html", error = "Wrong username or password")
        session["user_id"] = user["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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
    user_id=database.create_user(data["username"], data["password"])
    if user_id is None:
        return jsonify({"error": "That username is already taken."}), 400
    session["user_id"] = user_id
    return jsonify({"username": data["username"]})

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
    lang  = request.args.get(translations.translate("lang", "en"))
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

if __name__ == "__main__":
    app.run(debug=True, port=5002)
