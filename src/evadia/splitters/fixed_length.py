# evadia/splitters/instructor.py
from dataclasses import dataclass
from evadia.splitters.base import Splitter, SplitterConfigBase

@dataclass
class FixedLengthConfig(SplitterConfigBase):
    length: int = 100

class FixedLengthSplitter(Splitter):
    def __init__(self, config: FixedLengthConfig): 
        self.config = config
    def split(self, text: str) -> list[str]:
        """Splits text into chunks of fixed length."""
        length = self.config.length
        return [text[i:i + length] for i in range(0, len(text), length)]