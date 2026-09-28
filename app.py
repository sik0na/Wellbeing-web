from flask import Flask, render_template, request, redirect, session
import joblib
import content
import database


model = joblib.load("emotion_model.joblib")

database.create_tables()

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/checkin", methods = ["POST"])
def checkin():
    text = request.form["text"]
    emotion = model.predict([text])[0]
    return render_template("result.html", text=text, emotion=emotion, emotions=content.EMOTIONS)

@app.route("/message", methods = ["POST"])
def message():
    chosen=request.form["chosen"]
    text = request.form["text"]
    predicted = request.form["predicted"]
    return render_template("message.html", emotion=content.EMOTIONS[chosen],
                        text = text, predicted=predicted, chosen=chosen)

@app.route("/save", methods = ["POST"])
def save():
    database.save_checkin(request.form["text"], request.form["predicted"],
                          request.form["chosen"])
    return redirect("/history")


@app.route("/history")
def history():
    return render_template("history.html", checkin=database.get_all_checkins(),
                           emotion=content.EMOTIONS)

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

if __name__ == "__main__":
    app.run(debug=True, port=5002)