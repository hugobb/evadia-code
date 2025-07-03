# splitters/__init__.py

from .base import Splitter, SplitterConfigBase
from .basic import BasicConfig, BasicSplitter
from .basic2 import Basic2Config, Basic2Splitter

from typing import Type, Union

# Explicitly list all supported configs for type safety
SplitterConfig = Union[BasicConfig, Basic2Config]

# Registry maps config class → splitter class
_SPLITTER_REGISTRY: dict[Type[SplitterConfigBase], Type[Splitter]] = {
    BasicConfig: BasicSplitter,
    Basic2Config: Basic2Splitter,
}

def load_splitter(cfg: SplitterConfig) -> Splitter:
    print(f"Loading splitter with config: {type(cfg)}")
    splitter_cls = _SPLITTER_REGISTRY.get(type(cfg))
    if splitter_cls is None:
        raise ValueError(f"Unknown splitter config: {type(cfg)}")
    return splitter_cls(cfg)
