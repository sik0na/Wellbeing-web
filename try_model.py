import joblib

model = joblib.load("emotion_model.joblib")   # load the saved model

sentences = [
    "I'm worried about my exams",
    "I have no friends here",
    "Today was a great day",
]
for sentence in sentences:
    print(sentence, "->", model.predict([sentence])[0])