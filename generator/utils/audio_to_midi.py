import os
import shutil

from generator.utils.basic_pitch_process import basic_pitch
from generator.utils.clean_midi import clean_midi
from constants.paths import MIDI_PATH


def process_audio(audio_path: str) -> str:
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    dir_midi = os.path.join(MIDI_PATH, base_name)

    if os.path.exists(dir_midi):
        shutil.rmtree(dir_midi)

    basic_pitch([audio_path], dir_midi)
    midi_filename = os.path.join(dir_midi, f"{base_name}_basic_pitch.mid")

    return midi_filename
