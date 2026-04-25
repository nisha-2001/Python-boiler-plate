import logging
import base64
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class Base64FileRequest(BaseModel):
    file: str


@router.post("/read-file-data")
async def upload_file(request: Base64FileRequest = Body(...)):
    try:
        decoded_content = base64.b64decode(request.file)

        logger.info("200")

        return {
            "error": False,
            "message": "Base64 file received",
        }

    except Exception as exc:
        logger.error("Error decoding base64 file: %s", exc)
        raise HTTPException(status_code=400, detail="Invalid base64 content")
