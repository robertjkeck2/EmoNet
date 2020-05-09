import librosa
import numpy as np


def calculate_mel_frequency_cepstral_coefficients(file, num_coefs):
    raw_audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mfc_coefs = np.mean(librosa.feature.mfcc(
        y=raw_audio, sr=sample_rate, n_mfcc=num_coefs).T, axis=0)
    return mfc_coefs
