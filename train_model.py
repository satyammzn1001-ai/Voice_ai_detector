import os
import librosa
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

DATA_DIR = "data"
LANGS = ["english", "hindi", "tamil", "telugu", "malayalam"]

def extract_features(path):
    y, sr = librosa.load(path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfcc.T, axis=0)

X, y = [], []

for label, cls in enumerate(["human", "ai"]):
    for lang in LANGS:
        folder = os.path.join(DATA_DIR, cls, lang)
        if not os.path.isdir(folder):
            continue
        for file in os.listdir(folder):
            if file.endswith((".mp3", ".wav", ".flac")):
                try:
                    feat = extract_features(os.path.join(folder, file))
                    X.append(feat)
                    y.append(label)
                except:
                    pass

X = np.array(X)
y = np.array(y)

print("Total samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

acc = model.score(X_test, y_test)
print("Accuracy:", acc)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved as model.pkl")
