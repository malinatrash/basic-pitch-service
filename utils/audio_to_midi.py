import os
import shutil
import subprocess
from typing import Optional

from utils.basic_pitch_process import basic_pitch
from constants.paths import MIDI_PATH
from utils.logger import default_logger as logger


class AudioProcessingError(Exception):
    """Custom exception for audio processing errors"""
    pass


def convert_to_wav(input_path: str) -> str:
    """Convert audio file to WAV format using ffmpeg

    Args:
        input_path (str): Path to input audio file

    Returns:
        str: Path to converted WAV file

    Raises:
        AudioProcessingError: If conversion fails
    """
    output_path = os.path.splitext(input_path)[0] + '.wav'
    try:
        cmd = ['ffmpeg', '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_path, '-y']
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode != 0:
            raise AudioProcessingError(f"FFmpeg conversion failed: {process.stderr}")
        return output_path
    except subprocess.SubprocessError as e:
        raise AudioProcessingError(f"FFmpeg error: {str(e)}")
    except Exception as e:
        raise AudioProcessingError(f"Conversion error: {str(e)}")


def process_audio(audio_path: str) -> str:
    """Process audio file and convert it to MIDI

    Args:
        audio_path (str): Path to the input audio file

    Returns:
        str: Path to the generated MIDI file

    Raises:
        AudioProcessingError: If there's an error during processing
        FileNotFoundError: If the input audio file doesn't exist
    """
    wav_path = None
    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Input audio file not found: {audio_path}")

        logger.info(f"Starting audio processing for file: {audio_path}")
        file_ext = os.path.splitext(audio_path)[1].lower()

        # Convert non-wav files to wav format first
        if file_ext != '.wav':
            logger.info(f"Converting {file_ext} to WAV format")
            wav_path = convert_to_wav(audio_path)
            processing_path = wav_path
        else:
            processing_path = audio_path

        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        dir_midi = os.path.join(MIDI_PATH, base_name)

        if os.path.exists(dir_midi):
            logger.debug(f"Removing existing MIDI directory: {dir_midi}")
            shutil.rmtree(dir_midi)

        logger.info("Running Basic Pitch conversion")
        basic_pitch([processing_path], dir_midi)

        midi_filename = os.path.join(dir_midi, f"{base_name}_basic_pitch.mid")
        
        if not os.path.exists(midi_filename):
            raise AudioProcessingError("MIDI file was not generated successfully")

        logger.info(f"Successfully generated MIDI file: {midi_filename}")
        return midi_filename

    except AudioProcessingError:
        raise
    except Exception as e:
        logger.error(f"Error processing audio file: {str(e)}", exc_info=True)
        raise AudioProcessingError(f"Failed to process audio: {str(e)}") from e
    finally:
        # Clean up temporary WAV file if it was created
        if wav_path and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
                logger.debug(f"Removed temporary WAV file: {wav_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary WAV file: {str(e)}")
