import os.path
import uuid

from fastapi import UploadFile

from src.core.config import MEDIA_DIR


class UploadImageService:
    async def upload_image(self, image: UploadFile):
        filename = image.filename.split(".")
        path_url = f"{filename[0]}-{uuid.uuid4()}.{filename[-1]}"
        async with open(MEDIA_DIR / path_url, "wb") as f:
            f.write(image.file.read())

        return path_url

    async def delete_image(self, path_url):
        if os.path.exists(path_url):
            os.remove(path_url)
            return True
        return False
