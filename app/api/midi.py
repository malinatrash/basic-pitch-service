from fastapi import APIRouter, UploadFile
from starlette.responses import JSONResponse

from app.services.midi import MidiService

router = APIRouter(
    prefix="/midi",
    tags=["midi"],
    responses={404: {"description": "Not found"}, 500: {"description": "Internal Server Error"}, 403: {"description": "Forbidden"}},
)


@router.get("/")
def get_midi():
    return JSONResponse(content={"error": "unimplemented"}, status_code=500)


@router.post("/")
async def create_midi(file: UploadFile):
    return await MidiService.create_midi(file)

