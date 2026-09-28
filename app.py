from flask import Flask, render_template, request, redirect
import joblib
import content
import database


model = joblib.load("emotion_model.joblib")

database.create_tables()

app = Flask(__name__)


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
    return redirect("/history")
def history():
    return render_template("history.html", checkin=database.get_all_checkins(),
                           emotion=content.EMOTIONS)


if __name__ == "__main__":
    app.run(debug=True, port=5002)