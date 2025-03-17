from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.services.notes import NoteService

router = APIRouter(
    prefix="/notes",
)


@router.get("/id")
async def get_notes(note_id: int):
    notes = NoteService.get_notes_by_id(note_id)

    if notes is None:
        raise HTTPException(status_code=404, detail="Tabulature not found")

    return JSONResponse(content=notes, status_code=200)