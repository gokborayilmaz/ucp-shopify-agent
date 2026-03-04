from abc import ABC, abstractmethod
from typing import Any
from openai import OpenAI


class BaseAgent(ABC):
    def __init__(self, client: OpenAI):
        self.client = client

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        pass
