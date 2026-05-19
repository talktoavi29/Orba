from fastapi import APIRouter, HTTPException
from models.word_model import WordResponse, WordRequest, PracticeRequest, PracticeResponse, ReviewWord
from services.word_service import WordService
from services import srs_service
from typing import List

router = APIRouter(prefix="/word", tags=["Word"])

srs_service.init_db()
word_service = WordService()


@router.post("/lookup", response_model=WordResponse)
def lookup_word(request: WordRequest):
    try:
        return word_service.get_word_info(request.word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/practice", response_model=PracticeResponse)
def practice_word(request: PracticeRequest):

    try:
        correct, feedback = word_service.judge_practice(request.word, request.sentence)
        srs_service.record_attempt(request.word, correct)
        return PracticeResponse(correct=correct, feedback=feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review", response_model=List[ReviewWord])
def get_review_words():
    try:
        return srs_service.get_due_words()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
