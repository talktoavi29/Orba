from fastapi import APIRouter, HTTPException
from models.word_model import WordResponse, WordRequest
from services.word_service import WordService

router = APIRouter(prefix = "/word", tags=["Word"])

word_service = WordService()

@router.post("/lookup", response_model = WordResponse)
def lookup_word(request: WordRequest):
    try:
        return word_service.get_word_info(request.word)
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))