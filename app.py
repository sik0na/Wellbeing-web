from flask import Flask, render_template, request
import joblib
import content

model = joblib.load("emotion_model.joblib")

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


if __name__ == "__main__":
    app.run(debug=True, port=5002)