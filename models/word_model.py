from pydantic import BaseModel
from typing import List, Optional

class WordRequest(BaseModel):
    word:str

class RelatedWord(BaseModel):
    word:str
    similarity: float

class WordResponse(BaseModel):
    word:str
    definition: Optional[str]
    examples: List[str]
    related_words: List[RelatedWord]