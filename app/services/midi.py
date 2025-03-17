from fastapi import UploadFile
from starlette.responses import JSONResponse

from generator.controller import midi_to_tablature_json
from generator.utils.audio_to_midi import process_audio
from generator.utils.save_temp_file import save_temp_file
from models.midi import MidiFile
from models.notes import Notes


class MidiService:

    @staticmethod
    async def create_midi(file: UploadFile) -> JSONResponse:
        temp_file = await save_temp_file(file)
        result = MidiService.get_midi_by_file(temp_file)

        with open(result, 'rb') as f:
            midi_data = f.read()

        midi = MidiFile.create(file.filename, midi_data)

        records = midi_to_tablature_json(result)

        savedTabulature = Notes.create(midi.id, records)

        return JSONResponse(content={"id": savedTabulature.id, "tabs": str(records), "midi_id": midi.id}, status_code=200)

    @staticmethod
    def get_midi_by_file(audio_path: str) -> str:
        return process_audio(audio_path)
