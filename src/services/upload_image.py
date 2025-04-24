import os.path
import uuid

import aiofiles

from src.core.config import MEDIA_DIR


class UploadImageService:
    async def upload_image(self, chunks: bytes):
        filename = f"{uuid.uuid4().hex}.jpg"
        async with aiofiles.open(f"{MEDIA_DIR}/{filename}", "wb") as f:
            await f.write(chunks)

        return filename

    async def delete_image(self, filename):
        full_path = f"{MEDIA_DIR}/{filename}"
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
