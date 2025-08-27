import json
import os
from openai import OpenAI
from typing import List, Dict, Union
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

def call_llm(history: List[Dict[str, str]]) -> Union[ToolCall, FinalAnswer]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it with your OpenAI API key.")

    client = OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0,
                max_tokens=200,
            )
            raw = resp.choices[0].message.content.strip()

            # Parse the JSON response
            data = json.loads(raw)
            if data.get("type") == "final":
                return FinalAnswer(**data)
            return ToolCall(**data)

        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 1:  # Last attempt
                raise RuntimeError(f"LLM produced invalid JSON twice: {e}")
            # Add a message asking for valid JSON and retry
            messages.append({"role": "user", "content": "Please output valid JSON only."})
        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {e}")
