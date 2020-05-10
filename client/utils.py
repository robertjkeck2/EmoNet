import random

import librosa
import numpy as np
import requests

from model import EmoNet


EMOTIONS = {
    "calmness": 1,
    "happiness": 2,
    "sadness": 3,
    "anger": 4,
    "fear": 5,
    "disgust": 6,
    "surprise": 7
}
emonet = EmoNet()


def calculate_mel_frequency_cepstral_coefficients(file, num_coefs):
    raw_audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mfc_coefs = np.mean(librosa.feature.mfcc(
        y=raw_audio, sr=sample_rate, n_mfcc=num_coefs).T, axis=0)
    return mfc_coefs


def get_prompt():
    emotion, val = random.choice(list(EMOTIONS.items()))
    return {"emotion": emotion, "val": val}


def get_net_from_server():
    url = "http://localhost:8000/api/v1/send-model"
    with requests.post(url, stream=True) as r:
        r.raise_for_status()
        with open("data/model.h5", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    net = emonet.from_file("data/model.h5")
    return net

def send_update_to_server(net):
    net.save("data/model.h5")
    url = "http://localhost:8000/api/v1/receive-update"
    files = {"file": open("data/model.h5","rb")}
    requests.post(url, files = files)