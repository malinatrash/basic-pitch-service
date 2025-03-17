from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.services.track import TrackService

router = APIRouter(
    prefix="/tracks",
)


@router.get("/id")
async def get_track(track_id: int):
    track = TrackService.get_track_by_id(track_id)

    if track is None:
        raise HTTPException(status_code=404, detail="Track not found")

    return JSONResponse(content=track, status_code=200)


@router.post("/")
async def create_track():

    TrackService.create_track()