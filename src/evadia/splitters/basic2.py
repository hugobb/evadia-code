# evadia/splitters/instructor.py
from dataclasses import dataclass
from evadia.splitters.base import Splitter, SplitterConfigBase

@dataclass
class Basic2Config(SplitterConfigBase):
    ...

class Basic2Splitter(Splitter):
    def __init__(self, config: Basic2Config): 
        self.config = config
    def split(self, text: str) -> list[str]: return text.split(",")