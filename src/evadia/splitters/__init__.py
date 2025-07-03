# splitters/__init__.py

from .base import Splitter, SplitterConfigBase
from .basic import BasicConfig, BasicSplitter
from .fixed_length import FixedLengthConfig, FixedLengthSplitter
from .hugging_face import HuggingFaceConfig, HuggingFaceSplitter
from .ollama import OllamaConfig, OllamaSplitter

from typing import Type

# Explicitly list all supported configs for type safety
SplitterConfig = BasicConfig | FixedLengthConfig | HuggingFaceConfig | OllamaConfig

# Registry maps config class → splitter class
_SPLITTER_REGISTRY: dict[Type[SplitterConfigBase], Type[Splitter]] = {
    BasicConfig: BasicSplitter,
    FixedLengthConfig: FixedLengthSplitter,
    HuggingFaceConfig: HuggingFaceSplitter,
    OllamaConfig: OllamaSplitter,
}

def load_splitter(cfg: SplitterConfig) -> Splitter:
    splitter_cls = _SPLITTER_REGISTRY.get(type(cfg))
    if splitter_cls is None:
        raise ValueError(f"Unknown splitter config: {type(cfg)}")
    return splitter_cls(cfg)
