from utils.lib import get_midi_info
from utils.basic_pitch_process import basic_pitch
from utils.audio_to_midi import process_audio, AudioProcessingError
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from utils.logger import default_logger as logger
import tempfile
import os
import shutil
import time
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure FastAPI application
title = "Basic Pitch"
description = "Сервис преобразования аудио в MIDI"
app = FastAPI(
    title=title,
    description=description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
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
    request_id = f"req_{int(time.time()*1000)}"

    try:
        logger.info(f"[{request_id}] Начало обработки файла: {file.filename}")
        
        # Проверка формата файла
        allowed_formats = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in allowed_formats:
            logger.warning(f"[{request_id}] Попытка загрузки неподдерживаемого формата: {file_ext}")
            return JSONResponse(
                content={
                    "error": f"Неподдерживаемый формат файла. Поддерживаются только: {', '.join(allowed_formats)}"
                },
                status_code=400
            )

        # Создание временной директории и сохранение файла
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        logger.debug(f"[{request_id}] Создана временная директория: {temp_dir}")

        try:
            with open(temp_file_path, "wb") as temp_file:
                content = await file.read()
                temp_file.write(content)
            logger.debug(f"[{request_id}] Файл успешно сохранен: {temp_file_path}")
        except Exception as e:
            logger.error(f"[{request_id}] Ошибка при сохранении файла: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

        # Обработка аудио в MIDI
        try:
            midi_path = process_audio(temp_file_path)
            logger.info(f"[{request_id}] MIDI файл успешно создан: {midi_path}")
        except AudioProcessingError as e:
            logger.error(f"[{request_id}] Ошибка при обработке аудио: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"[{request_id}] Неожиданная ошибка при обработке аудио: {str(e)}")
            raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

        # Получение информации о MIDI
        try:
            midi_info = get_midi_info(midi_path)
            logger.debug(f"[{request_id}] Получена информация о MIDI: {midi_info}")
        except Exception as e:
            logger.warning(f"[{request_id}] Ошибка при получении информации о MIDI: {str(e)}")
            midi_info = {"note_count": 0, "error": str(e)}

        output_filename = os.path.splitext(file.filename)[0] + ".mid"
        background_tasks.add_task(clean_temp_files, temp_dir)

        processing_time = time.time() - start_time
        logger.info(
            f"[{request_id}] Обработка завершена за {processing_time:.2f} секунд. "
            f"Создан MIDI с {midi_info.get('note_count', 0)} нотами."
        )

        return FileResponse(
            path=midi_path,
            filename=output_filename,
            media_type="audio/midi"
        )

    except Exception as e:
        logger.error(f"[{request_id}] Критическая ошибка: {str(e)}", exc_info=True)
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
