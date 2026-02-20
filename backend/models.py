from pydantic import BaseModel
from typing import List, Optional

class OptimizeRequest(BaseModel):
    input: str
    style: Optional[str] = "professional"

class ScrapeRequest(BaseModel):
    url: str
    query: str

class Prompt(BaseModel):
    id: str
    title: str
    original: str
    optimized: str
    tags: List[str]
    model: str = "gpt-4o"
    rating: float = 5.0
    created: str
    uses: int = 0