# splitters/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class SplitterConfigBase():
    pass

class Splitter(ABC):
    def __init__(self, config: SplitterConfigBase):
        self.config = config

    @abstractmethod
    def split(self, text: str) -> list[str]:
        ...
