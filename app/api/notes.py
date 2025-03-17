from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from models.notes import Notes
from models.track import Track

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.patch("/id")
async def update_notes(note_id: int, notes: dict, tempo: int = None):
    notes = Notes.update(id=note_id, notes=notes, tempo=tempo)

    if notes is None:
        raise HTTPException(status_code=404, detail="Tabulature not found")

    return JSONResponse(content={
        "id": notes.id,
        "notes": notes.notes_id,
        "tempo": notes.tempo
    }, status_code=200)


@router.get("/id")
async def get_notes_by_id(note_id: int):
    notes = Notes.get(note_id)

    if notes is None:
        raise HTTPException(status_code=404, detail="Tabulature not found")

    return JSONResponse(content={
        "id": notes.id,
        "notes": notes.notes_id,
        "tempo": notes.tempo
    }, status_code=200)


@router.get("/id")
async def get_notes_by_track_id(track_id: int):
    track = Track.get(track_id)

    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    notes = Notes.get(track.notes_id)

    if notes is None:
        raise HTTPException(status_code=404, detail="Tabulature not found")

    return JSONResponse(content={
        "id": notes.id,
        "notes": notes.notes_id,
        "tempo": notes.tempo
    }, status_code=200)