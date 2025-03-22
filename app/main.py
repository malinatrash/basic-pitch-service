from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
import tempfile
import os
import shutil
import time
import sys

# Добавляем путь к корневой директории проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.audio_to_midi import process_audio
from utils.basic_pitch_process import basic_pitch
from utils.lib import get_midi_info

title = "Basic Pitch"
description = "Сервис преобразования аудио в MIDI"
app = FastAPI(title=title, description=description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/audio-to-midi")
async def audio_to_midi(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Преобразование аудиофайла в MIDI файл"""
    start_time = time.time()
    temp_dir = None
    
    try:
        allowed_formats = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_formats:
            return JSONResponse(
                content={"error": f"Неподдерживаемый формат файла. Поддерживаются только: {', '.join(allowed_formats)}"},
                status_code=400
            )
        
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        
        # Проверяем, что process_audio успешно выполнена
        try:
            midi_path = process_audio(temp_file_path)
            if not os.path.exists(midi_path):
                return JSONResponse(
                    content={"error": f"Не удалось создать MIDI файл: файл не найден"},
                    status_code=500
                )
        except Exception as e:
            return JSONResponse(
                content={"error": f"Ошибка при обработке аудио в MIDI: {str(e)}"},
                status_code=500
            )
        
        # Получаем информацию о MIDI
        try:
            midi_info = get_midi_info(midi_path)
        except Exception as e:
            midi_info = {"note_count": 0, "error": str(e)}
        
        output_filename = os.path.splitext(file.filename)[0] + ".mid"
        
        # Добавляем задачу на удаление временных файлов
        background_tasks.add_task(clean_temp_files, temp_dir)
        
        processing_time = time.time() - start_time
        print(f"Аудиофайл обработан за {processing_time:.2f} секунд. Создан MIDI с {midi_info.get('note_count', 0)} нотами.")
        
        return FileResponse(
            path=midi_path,
            filename=output_filename,
            media_type="audio/midi"
        )
        
    except Exception as e:
        if temp_dir and os.path.exists(temp_dir):
            clean_temp_files(temp_dir)
        return JSONResponse(
            content={"error": f"Ошибка при обработке аудиофайла: {str(e)}"}, 
            status_code=500
        )


@app.get("/")
async def root():
    """Корневой эндпоинт, возвращающий информацию о сервисе"""
    return {
        "name": title,
        "description": description,
        "endpoints": [
            {
                "path": "/audio-to-midi",
                "method": "POST",
                "description": "Преобразование аудиофайла в MIDI формат",
                "supported_formats": [".wav", ".mp3", ".ogg", ".flac"]
            }
        ]
    }


def clean_temp_files(temp_dir):
    """Функция для очистки временных файлов"""
    try:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Ошибка при очистке временных файлов: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
