from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class WordRequest(BaseModel):
    word: str

class RelatedWord(BaseModel):
    word: str
    similarity: float

class Meaning(BaseModel):
    definition: str
    examples: List[str]

class WordResponse(BaseModel):
    word: str
    meanings: List[Meaning]
    related_words: List[RelatedWord]

class PracticeRequest(BaseModel):
    word: str
    sentence: str

class PracticeResponse(BaseModel):
    correct: bool
    feedback: str

class ReviewWord(BaseModel):
    word: str
    next_review: date
    interval_days: int
    ease_factor: float