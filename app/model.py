import numpy as np
import librosa
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def extract_features(y, sr=16000):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfcc.T, axis=0)

def predict(audio):
    feat = extract_features(audio).reshape(1, -1)
    prob = model.predict_proba(feat)[0][1]

    if prob > 0.5:
        return "AI_GENERATED", float(prob)
    else:
        return "HUMAN", float(1 - prob)
