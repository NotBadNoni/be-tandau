from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile, File

from src.schemas.image import ImageResponse
from src.services.upload_image import UploadImageService

router = APIRouter()


@router.post('/upload', response_model=ImageResponse)
@inject
async def upload_image(upload_service: FromDishka[UploadImageService], image: UploadFile = File(...)):
    return await upload_service.upload_image(image)


@router.delete('/delete')
@inject
async def delete_image(image_name: str, upload_service: FromDishka[UploadImageService]):
    return await upload_service.delete_image(image_name)
