from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    type: str = Field(default="tool", frozen=True)
    tool: str
    args: dict

class FinalAnswer(BaseModel):
    type: str = Field(default="final", frozen=True)
    content: str
