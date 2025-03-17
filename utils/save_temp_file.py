import os
import time

from fastapi import UploadFile

from constants.paths import STOCK_PATH


async def save_temp_file(file: UploadFile) -> str:
    temp_folder = os.path.join(STOCK_PATH, str(time.time()))
    os.makedirs(temp_folder, exist_ok=True)

    temp_file = os.path.join(temp_folder, file.filename)

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    return temp_file


def create_empty_file() -> str:
    temp_folder = os.path.join(STOCK_PATH, str(time.time()))
    os.makedirs(temp_folder, exist_ok=True)

    temp_file = os.path.join(temp_folder, "empty_file")
    with open(temp_file, "w") as f:
        pass

    return temp_file
