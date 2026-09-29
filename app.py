from flask import Flask, render_template, request, redirect, session, jsonify
import joblib
import content
import database


model = joblib.load("emotion_model.joblib")

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
    emotion = model.predict([text])[0]
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


if __name__ == "__main__":
    app.run(debug=True, port=5002)