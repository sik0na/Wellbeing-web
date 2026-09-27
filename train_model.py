import csv 
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

texts= []
labels = []
with open("data/emotions.csv", encoding = "utf-8") as f:
    for row in csv.DictReader(f):
        texts.append(row["text"])
        labels.append(row["label"])
print("Sentences:", len(texts))

train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size = 0.2, random_state = 42, stratify = labels)


model = Pipeline([
    ("features",  TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])
model.fit(train_texts, train_labels)

predictions = model.predict(test_texts)
print("Accuracy:", model.score(test_texts, test_labels))

joblib.dump(model, "emotion_model.joblib")
print("Saved emotion_model.joblib")