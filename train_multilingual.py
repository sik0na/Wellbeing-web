import csv
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

ENCODER_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def load_csv(path):
    texts, labels = [], []
    with open(path, encoding = "utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels

student_texts, student_labels = load_csv("data/emotions.csv")
go_texts, go_labels = load_csv("data/goemotions_train.csv")
texts = student_texts + go_texts
labels = student_labels + go_labels

weights = [10] * len(student_texts) + [1] * len(go_texts)

print("Loading the HuggingFace model...")
encoder = SentenceTransformer(ENCODER_NAME)

print("Turning", len(texts), "sentences into numbers (takes a minute)...")
numbers = encoder.encode(texts, batch_size = 64, normalize_embeddings = True)

classifier = LogisticRegression(max_iter = 3000, class_weight = "balanced")
classifier.fit(numbers, labels, sample_weight = weights)

for language, path in [("English", "data/student_test.csv"),
                       ("Hungarian", "data/student_test_hu.csv"),
                       ("Mongolian", "data/student_test_mn.csv")]:
    test_texts, test_labels = load_csv(path)
    predictions = classifier.predict(encoder.encode(test_texts, normalize_embeddings = True))
    print(f"{language:10} accuracy: {accuracy_score(test_labels, predictions):.2f}")

joblib.dump(classifier, "emotion_model_multi.joblib")
print("Saved emotion_model_multi.joblib")