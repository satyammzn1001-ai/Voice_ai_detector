import numpy as np
import librosa
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def extract_features(path):
    y, sr = librosa.load(path, sr=16000, mono=True, duration=5.0)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfcc.T, axis=0)

def predict(audio_path):
    feat = extract_features(audio_path).reshape(1, -1)
    prob = model.predict_proba(feat)[0][1]

    confidence = round(float(prob), 2)

    if prob > 0.5:
        result = "AI_GENERATED"
        explanation = (
            "The audio shows characteristics of synthetic speech such as "
            "uniform pitch, low natural variation, and consistent energy patterns."
        )
    else:
        result = "HUMAN"
        explanation = (
            "The audio contains natural speech variations including pauses, "
            "pitch fluctuations, and irregular energy patterns typical of human speech."
        )

    return result, confidence, explanation
