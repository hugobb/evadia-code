# evadia/splitters/instructor.py
from dataclasses import dataclass
from evadia.splitters.base import Splitter, SplitterConfigBase

@dataclass
class BasicConfig(SplitterConfigBase):
    ...

class BasicSplitter(Splitter):
    def __init__(self, config: BasicConfig): 
        self.config = config
    def split(self, text: str) -> list[str]: return text.split(",")