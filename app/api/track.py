from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from models.instruments import Instrument
from models.track import Track

router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
)


@router.get("/id")
async def get_track(track_id: int):
    track = Track.get(track_id)

    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    instrument = Instrument.get_by_id(track.instrument_id)
    return JSONResponse(content={
        "id": track.id,
        "name": track.name,
        "instrument": instrument.name
    }, status_code=200)


@router.post("/")
async def create_track(instrument: str, name: str):
    try:
        track_id = Track.create(name, instrument)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={
        "id": track_id,
    }, status_code=201)
