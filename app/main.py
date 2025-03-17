from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import midi, notes, track
from config.origins import origins

title = "Basic Pitch"
description = "Сервис генерации гитарных табулатур"
app = FastAPI(title=title, description=description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(midi.router)
app.include_router(notes.router)
app.include_router(track.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
