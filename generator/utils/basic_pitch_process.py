import os

from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

minimum_frequency = 50
maximum_frequency = 2000


def basic_pitch(input_audio_paths: list, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    predict_and_save(
        input_audio_paths,
        output_directory,
        maximum_frequency=maximum_frequency,
        minimum_frequency=minimum_frequency,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
    )