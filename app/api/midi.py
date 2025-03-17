from fastapi import APIRouter, UploadFile
from starlette.responses import JSONResponse

from models.midi import MidiFile
from models.notes import Notes
from models.track import Track
from utils.lib import midi_to_tablature_json, midi_to_tempo

router = APIRouter(
    prefix="/midi",
    tags=["midi"],
)


@router.post("/")
async def create_midi(track_id: int, file: UploadFile):
    try:
        midi_file = MidiFile.create(file.filename, await file.read(), file.filename)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    try:
        notes = midi_to_tablature_json(file.filename)
        tempo = midi_to_tempo(await file.read())

        notes_data = await Notes.create(midi_file.id, notes, tempo)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    try:
        await Track.add_notes(track_id, notes_data.id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={
        "notes_id": notes_data.id,
        "notes": notes,
        "tempo": tempo,
        "track_id": track_id
    }, status_code=200)



