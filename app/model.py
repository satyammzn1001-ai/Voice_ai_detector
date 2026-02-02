def predict(audio):
    duration = len(audio) / 16000

    if duration < 3:
        return "AI_GENERATED", 0.81
    else:
        return "HUMAN", 0.67
