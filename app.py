from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return 'Hello! This is my wellbeing app. <a href="/about">About</a>'


@app.route("/about")
def about():
    return "This is the about page."


if __name__ == "__main__":
    app.run(debug=True, port=5002)