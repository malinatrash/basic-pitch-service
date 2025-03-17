from typing import Any

import mido
from fastapi import HTTPException
from starlette.responses import JSONResponse

from models.notes import Notes


async def get_tabulature_by_id(tabulature_id) -> JSONResponse:
    tabulature = Notes.get(tabulature_id)

    if tabulature is None:
        raise HTTPException(status_code=404, detail="Tabulature not found")

    res = {
        "id": tabulature.id,
        "midi_id": tabulature.midi_id,
        "tabs": tabulature.notes,
        "xml": tabulature.xml
    }

    return JSONResponse(content=res, status_code=200)


def midi_to_tablature_json(midi_path) -> list[dict[str, Any]]:
    file = mido.MidiFile(midi_path)

    note_array = []
    for msg in file:
        if msg.type == 'note_on':
            record = {
                "note": msg.note,
                "velocity": msg.velocity,
                "time": msg.time,
                "duration": msg.time,
                "channel": msg.channel,
            }
            note_array.append(record)

    print(note_array)
    return note_array
