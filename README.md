# Agent Toolpicker – Single-Turn ReAct CLI

A minimal, zero-dependency* CLI agent that decides—**in a single turn**—whether to
invoke a symbolic calculator (SymPy) or return a plain-text answer.

\* *Except for the OpenAI client, Pydantic, SymPy and Pytest.*

---

## Features

- **Single-turn ReAct** – no iterative loop; one LLM call, one tool call.
- **Two built-in tools**  
  1. **Calculator** – solves arithmetic / symbolic math via SymPy.  
  2. **Text responder** – returns direct natural-language answers.
- **Strict schema** – every agent response is validated with Pydantic.
- **Extensible** – drop-in new tools by adding functions to `tools.py`.
- **Tested** – 100 % unit-test coverage via Pytest.

---

## Scripts

### Core Scripts

#### `agent.py`
The main CLI entry point for the agent. Orchestrates the conversation flow and tool execution.

**Usage:**
```bash
python agent.py "your question here"
python agent.py "your question here" --verbose  # Show decision process
```

**Features:**
- Accepts natural language questions as command-line arguments
- Supports verbose mode (`-v` or `--verbose`) to show the agent's decision-making process
- Runs up to 3 steps of ReAct (Reasoning and Acting) before timing out
- Handles tool calls and provides final answers

#### `policy.py`
Contains the LLM policy that decides whether to use tools or provide direct answers.

**Key components:**
- `call_llm()`: Interfaces with OpenAI's GPT-4o-mini model
- System prompt that defines available tools and response format
- JSON response parsing and validation
- Automatic retry logic for malformed responses

#### `tools.py`
Defines the available tools and their implementations.

**Available tools:**
- **calculator**: Evaluates mathematical expressions using SymPy
- **reverse_string**: Reverses input text
- **word_count**: Counts words in input text

**Tool structure:**
- Each tool has a name, JSON schema, and callable function
- Safe execution with error handling
- Extensible design for adding new tools

#### `io_models.py`
Pydantic models for structured input/output validation.

**Models:**
- `ToolCall`: Represents a tool invocation with name and arguments
- `FinalAnswer`: Represents the agent's final response to the user

### Setup and Testing Scripts

#### `setup.sh`
Setup script that checks environment configuration and runs tests.

**Features:**
- Checks if `OPENAI_API_KEY` environment variable is set
- Provides setup instructions if API key is missing
- Automatically runs tests if environment is properly configured

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

#### `run_tests.py`
Test suite using pytest to validate agent functionality.

**Test cases:**
- `test_17_times_23()`: Tests mathematical calculation (17 × 23 = 391)
- `test_reverse()`: Tests string reversal ("pineapple" → "elppaenip")
- `test_wordcount()`: Tests word counting ("to be or not to be" → 6 words)

**Usage:**
```bash
python run_tests.py
# or
pytest run_tests.py -v
```

---

## Quick start

```bash
# 1. Clone
git clone <repository url>

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Export your OpenAI key
export OPENAI_API_KEY="sk-your-key-here"   # Windows: set OPENAI_API_KEY=...

# 5. Run
python agent.py "What is the integral of x^2 from 0 to 1?"

# 6. Verbose mode
python agent.py "Compute sin(pi/4)" --verbose

# 7 Run tests
python run_tests.py
```
