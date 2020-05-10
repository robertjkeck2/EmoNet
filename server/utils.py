import fnmatch
import os

import librosa
import numpy as np
from sklearn.model_selection import train_test_split

from config import (
    RAVDESS_FILENAME_FORMAT,
    RAVDESS_FILEPATH,
    SAVEE_FILENAME_FORMAT,
    SAVEE_FILEPATH,
    SAVEE_TO_RADVESS_CONVERSION
)


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
    print(file_params)
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


FILENAME_PARSERS = {
    "RAVDESS": parse_ravdess_filename,
    "SAVEE": parse_savee_filename,
}


def prepare_data(files, data_set, num_coefs):
    X = []
    y = []
    num_files = len(files)
    for i, f in enumerate(files):
        parsed_file = FILENAME_PARSERS[data_set](f)
        mfc_coefs = calculate_mel_frequency_cepstral_coefficients(
            parsed_file.get("filepath"), num_coefs)
        X.append(mfc_coefs)
        y.append(parsed_file.get("label"))
    return X, y


def initialize_ravdess_data(num_coefs):
    ravdess_files = []

    for actor in os.listdir(RAVDESS_FILEPATH):
        if actor not in (".DS_Store", "README.md"):
            for f in os.listdir(RAVDESS_FILEPATH / actor):
                ravdess_files.append(f)

    ravdess_X, ravdess_y = prepare_data(ravdess_files, "RAVDESS", num_coefs)

    X = np.asarray(ravdess_X)
    y = np.asarray(ravdess_y)

    np.savetxt(
        "data/RAVDESS_MFCC/X.csv".format(num_coefs), X, delimiter=",")
    np.savetxt(
        "data/RAVDESS_MFCC/y.csv".format(num_coefs), y, delimiter=",")


def initialize_savee_data(num_coefs):
    savee_files = [x for x in os.listdir(
        SAVEE_FILEPATH) if fnmatch.fnmatch(x, '*.wav')]
    savee_X, savee_y = prepare_data(savee_files, "SAVEE", num_coefs)
    np.savetxt("data/SAVEE_MFCC/X.csv".format(num_coefs),
               savee_X, delimiter=",")
    np.savetxt("data/SAVEE_MFCC/y.csv".format(num_coefs),
               savee_y, delimiter=",")


def load_dataset(num_coefs, train_pct, dataset="RAVDESS"):
    X = np.loadtxt(
        f"data/{dataset}_MFCC/X.csv", delimiter=',')
    y = np.loadtxt(
        f"data/{dataset}_MFCC/y.csv", delimiter=',')

    if train_pct is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=train_pct)
        X_train = np.expand_dims(X_train, axis=2)
        X_test = np.expand_dims(X_test, axis=2)
    else:
        X_train, X_test, y_train, y_test = X, np.array([]), y, np.array([])
        X_train = np.expand_dims(X_train, axis=2)

    return X_train, X_test, y_train, y_test


def average_weights(devices):
    weight_sum = sum(np.array(net.model.get_weights()) for net in devices)
    return weight_sum / len(devices)
