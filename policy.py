import json
import os
from abc import ABC, abstractmethod
from openai import OpenAI
from typing import List, Dict, Union, Optional
from pydantic import ValidationError
from io_models import ToolCall, FinalAnswer

SYSTEM_PROMPT = (
    "You are a helpful assistant that uses tools when needed.\n"
    "You must output ONLY valid JSON in one of these two formats:\n\n"
    "For tool usage:\n"
    '{"type": "tool", "tool": "tool_name", "args": {"param": "value"}}\n\n'
    "For final answers:\n"
    '{"type": "final", "content": "your answer"}\n\n'
    "Available tools:\n"
    "- calculator: for arithmetic expressions, args: {\"expression\": \"math_expression\"}\n"
    "- reverse_string: for reversing text, args: {\"text\": \"string_to_reverse\"}\n"
    "- word_count: for counting words, args: {\"text\": \"text_to_count\"}\n\n"
    "Examples:\n"
    'Question: "What is 5+3?" → {"type": "tool", "tool": "calculator", "args": {"expression": "5+3"}}\n'
    'Question: "Reverse hello" → {"type": "tool", "tool": "reverse_string", "args": {"text": "hello"}}\n'
    'Tool result: 8 → {"type": "final", "content": "8"}\n\n'
    "Remember: Output ONLY the JSON, nothing else."
)

class LLMWrapper(ABC):
    """Abstract base class for LLM wrappers"""
    def __init__(self, system_prompt: str = SYSTEM_PROMPT):
        self.system_prompt = system_prompt

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """Generate a response from the LLM"""
        pass

    def call(
        self,
        history: List[Dict[str, str]],
        max_retries: int = 2
    ) -> None | FinalAnswer | ToolCall:
        """Call the LLM and parse the response into ToolCall or FinalAnswer"""
        messages = [{"role": "system", "content": self.system_prompt}] + history

        for attempt in range(max_retries):
            try:
                raw = self.generate(messages)

                # Parse the JSON response
                data = json.loads(raw)
                if data.get("type") == "final":
                    return FinalAnswer(**data)
                return ToolCall(**data)

            except (json.JSONDecodeError, ValidationError) as e:
                if attempt == max_retries - 1:  # Last attempt
                    raise RuntimeError(f"LLM produced invalid JSON after {max_retries} attempts: {e}")
                # Add a message asking for valid JSON and retry
                messages.append({"role": "user", "content": "Please output valid JSON only."})
            except Exception as e:
                raise RuntimeError(f"Error calling LLM: {e}")


class OpenAIWrapper(LLMWrapper):
    """OpenAI LLM wrapper implementation"""
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0,
        max_tokens: int = 200,
        system_prompt: str = SYSTEM_PROMPT
    ):
        super().__init__(system_prompt)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set or api_key not provided. Please set it with your OpenAI API key.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """Generate a response using OpenAI's API"""
        # Allow override of default parameters
        model = kwargs.get('model', self.model)
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_tokens', self.max_tokens)

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()



# Default LLM instance for backward compatibility
_default_llm = None

def get_default_llm() -> LLMWrapper:
    """Get the default LLM instance (OpenAI by default)"""
    global _default_llm
    if _default_llm is None:
        _default_llm = OpenAIWrapper()
    return _default_llm

def set_default_llm(llm: LLMWrapper):
    """Set a custom default LLM instance"""
    global _default_llm
    _default_llm = llm

# Backward compatibility function
def call_llm(history: List[Dict[str, str]]) -> Union[ToolCall, FinalAnswer]:
    """Backward compatible function that uses the default LLM"""
    return get_default_llm().call(history)
