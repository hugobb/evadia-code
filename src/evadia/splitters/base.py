# splitters/base.py
from pydantic import BaseModel
from abc import ABC, abstractmethod

class SplitterConfigBase(BaseModel):
    pass

class Splitter(ABC):
    def __init__(self, config: SplitterConfigBase):
        self.config = config

    @abstractmethod
    def split(self, text: str) -> list[str]:
        ...
