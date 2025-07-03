from dataclasses import dataclass
from typing import List

from pydantic import BaseModel
from openai import OpenAI
import instructor

from .base import Splitter, SplitterConfigBase

@dataclass
class OllamaConfig(SplitterConfigBase):
    model: str = "mistral"
    base_url: str = "http://localhost:11434/v1"
    max_retries: int = 2
    timeout: float = 10.0

class IdeaList(BaseModel):
    ideas: List[str]

class OllamaSplitter(Splitter):
    def __init__(self, config: OllamaConfig):
        self.config = config
        self.client = instructor.from_openai(
            OpenAI(
                base_url=config.base_url,
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )

    def split(self, text: str) -> List[str]:
        response = self.client.chat.completions.create(
            model=self.config.model,
            response_model=IdeaList,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Extract the core ideas from the following sentence. "
                        "Return a list of simple, clear ideas:\n\n"
                        f"{text}"
                    ),
                }
            ],
            max_retries=self.config.max_retries,
            timeout=self.config.timeout,
        )
        return response.ideas
