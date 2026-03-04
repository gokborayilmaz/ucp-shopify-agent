from typing import List, Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str
    title: str
    price: float
    image: Optional[str] = None
    store_domain: str
    url: Optional[str] = None


class SearchIntent(BaseModel):
    keywords: List[str] = Field(default_factory=list)
    gender: str = "unisex"
    scenario: str = "standard"


class SearchResult(BaseModel):
    status: str
    products: List[Product] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
