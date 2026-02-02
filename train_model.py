import os
import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2Model

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
wav2vec = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")

for p in wav2vec.parameters():
    p.requires_grad = False

class Classifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = torch.nn.Linear(768, 1)

    def forward(self, x):
        x = x.mean(dim=1)
        return torch.sigmoid(self.fc(x))

model = Classifier()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.BCELoss()

def train_folder(folder, label):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if not path.endswith((".wav", ".mp3", ".flac")):
            continue

        audio, _ = librosa.load(path, sr=16000)
        inputs = processor(audio, return_tensors="pt", sampling_rate=16000)

        with torch.no_grad():
            feats = wav2vec(**inputs).last_hidden_state

        pred = model(feats)
        loss = loss_fn(pred, torch.tensor([[label]], dtype=torch.float))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

for _ in range(5):  # epochs
    for lang in os.listdir("data/human"):
        train_folder(f"data/human/{lang}", 0)
        train_folder(f"data/ai/{lang}", 1)

torch.save(model.state_dict(), "voice_ai_model.pt")
print("✅ Training complete, model saved")
