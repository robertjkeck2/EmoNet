import os

import librosa
import numpy as np

from config import (
    RAVDESS_FILENAME_FORMAT,
    RAVDESS_FILEPATH,
    SAVEE_FILENAME_FORMAT,
    SAVEE_FILEPATH,
    SAVEE_TO_RADVESS_CONVERSION
)


FILENAME_PARSERS = {
    "RAVDESS": parse_ravdess_filename,
    "SAVEE": parse_savee_filename,
}


def calculate_mel_frequency_cepstral_coefficients(file, num_coefs):
    raw_audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mfc_coefs = np.mean(librosa.feature.mfcc(
        y=raw_audio, sr=sample_rate, n_mfcc=num_coefs).T, axis=0)
    return mfc_coefs


def _ravdess_filename_helper(filename):
    file_params = os.path.splitext(filename)[0].split("-")
    sample = {}
    for param_name, param_info in RAVDESS_FILENAME_FORMAT.items():
        param_idx, param_map = param_info
        sample[param_name] = param_map[file_params[param_idx]]
    sample["label"] = int(file_params[2]) - 1
    return sample


def parse_ravdess_filename(filename, base_path=RAVDESS_FILEPATH):
    sample = _ravdess_filename_helper(filename)
    actor_num = str(sample['actor'][0]).zfill(2)
    return {
        "filepath": str(base_path / f"Actor_{actor_num}" / f"{filename}"),
        "label": sample["label"],
    }


def _savee_filename_helper(filename):
    file_params = os.path.splitext(filename)[0].split("_")
    file_params = (file_params[0], file_params[1][:-2])
    sample = {}
    for param_name, param_info in SAVEE_FILENAME_FORMAT.items():
        param_idx, param_map = param_info
        sample[param_name] = param_map[file_params[param_idx]]
    sample["label"] = SAVEE_TO_RADVESS_CONVERSION[sample['emotion']]
    return sample


def parse_savee_filename(filename):
    sample = _savee_filename_helper(filename)
    return {
        "filepath": str(SAVEE_FILEPATH / filename),
        "label": sample["label"],
    }
