from fastapi import APIRouter, Depends, HTTPException, status
from app.model.api import OCRRequest, OCRResponse
from app.services.ocr import OCRService
from app.utils.logger import logger

router = APIRouter(tags=["OCR processing"])


@router.post("/ocr-process", response_model=OCRResponse, status_code=status.HTTP_200_OK)
async def process_ocr(
    request_data: OCRRequest, service: OCRService = Depends(OCRService)
):
    path = request_data.file_name

    try:
        detected_texts = service.process_and_overwrite_image(file_name=path)

        return OCRResponse(status="success", file_name=path, found_texts=detected_texts)

    except ValueError as e:
        logger.error("Could not process image: %s, error: %s", path, str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not porcess file: {str(e)}",
        )
