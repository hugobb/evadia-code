from dataclasses import dataclass
from typing import List
import json

import torch
from pydantic import BaseModel, ValidationError
from transformers import AutoTokenizer, AutoModelForCausalLM

from .base import Splitter, SplitterConfigBase

@dataclass
class HuggingFaceConfig(SplitterConfigBase):
    model_name: str = "microsoft/Phi-3-mini-128k-instruct"
    max_tokens: int = 512
    temperature: float = 0.2

class IdeaList(BaseModel):
    ideas: List[str]

class HuggingFaceSplitter(Splitter):
    schema_model = IdeaList

    def __init__(self, config: HuggingFaceConfig):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

    def _make_prompt(self, text: str) -> str:
        example_values = {
            name: ["example1", "example2"]
            for name, field in self.schema_model.model_fields.items()
            if field.annotation == List[str]
        }

        schema_example = self.schema_model(**example_values)
        example_json = json.dumps(schema_example.model_dump(), indent=2)

        return (
            "Extract the main ideas from the sentence below.\n"
            "Return the output as valid JSON following this format:\n"
            f"{example_json}\n\n"
            f"Sentence: {text}\n\nJSON:"
        )

    def split(self, text: str) -> List[str]:
        prompt = self._make_prompt(text)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        json_start = decoded.find("{")
        json_part = decoded[json_start:] if json_start != -1 else decoded

        try:
            parsed = self.schema_model(**json_part)
            return parsed.ideas
        except ValidationError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"Raw output:\n{decoded}")
            return []
