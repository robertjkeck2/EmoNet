import os

RAVDESS_MODALITY = {
    "01": "full-AV",
    "02": "video-only",
    "03": "audio-only",
}
RAVDESS_VOCAL_CHANNEL = {
    "01": "speech",
    "02": "song",
}
RAVDESS_EMOTION = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised",
}
RAVDESS_EMOTIONAL_INTENSITY = {
    "01": "normal",
    "02": "strong",
}
RAVDESS_STATEMENT = {
    "01": "kids are talking by the door",
    "02": "dogs are sitting by the door",
}
RAVDESS_REPETITION = {
    "01": 1,
    "02": 2,
}


def RAVDESS_GENDER(i): return "female" if i % 2 == 0 else "male"


RAVDESS_ACTOR = {"{:02d}".format(i): (i, RAVDESS_GENDER(i))
                 for i in range(1, 25)}
RAVDESS_FILENAME_FORMAT = {
    "modality": (0, RAVDESS_MODALITY),
    "vocal_channel": (1, RAVDESS_VOCAL_CHANNEL),
    "emotion": (2, RAVDESS_EMOTION),
    "emotional_intensity": (3, RAVDESS_EMOTIONAL_INTENSITY),
    "statement": (4, RAVDESS_STATEMENT),
    "repetition": (5, RAVDESS_REPETITION),
    "actor": (6, RAVDESS_ACTOR),
}
SAVEE_ACTOR = {
    "DC": "DE",
    "JE": "JE",
    "JK": "JK",
    "KL": "JL",
}
SAVEE_EMOTION = {
    "a": "angry",
    "d": "disgust",
    "f": "fearful",
    "h": "happy",
    "n": "neutral",
    "sa": "sad",
    "su": "surprised"
}
SAVEE_TO_RADVESS_CONVERSION = {
    "angry": 4,
    "disgust": 6,
    "fearful": 5,
    "happy": 2,
    "neutral": 0,
    "sad": 3,
    "surprised": 7
}
SAVEE_FILENAME_FORMAT = {
    "actor": (0, SAVEE_ACTOR),
    "emotion": (1, SAVEE_EMOTION),
}


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
