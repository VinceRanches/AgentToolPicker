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
python agent.py --help                          # Show help and usage examples
```

**Options:**
- `question`: The question or task to ask the agent (required, use quotes for multi-word questions)
- `--verbose`, `-v`: Enable verbose output showing the agent's step-by-step decision process
- `--help`, `-h`: Show help message with usage examples and available options

**Features:**
- Accepts natural language questions as command-line arguments
- Supports verbose mode to show the agent's decision-making process
- Runs up to 3 steps of ReAct (Reasoning and Acting) before timing out
- Handles tool calls and provides final answers
- Comprehensive help documentation with examples

#### `policy.py`
LLM wrapper module that provides a flexible interface for different language models, with OpenAI as the default provider.

**Key components:**
- `LLMWrapper`: Abstract base class for implementing different LLM providers
- `OpenAIWrapper`: Default implementation using OpenAI's GPT-4o-mini model
- `call_llm()`: Backward-compatible function that uses the default LLM
- `get_default_llm()` / `set_default_llm()`: Functions to manage the default LLM instance

**Features:**
- Extensible design allowing easy integration of other LLM providers
- System prompt management for tool selection and response formatting
- JSON response parsing and validation with Pydantic models
- Automatic retry logic for malformed responses
- Configurable model parameters (temperature, max_tokens, etc.)
- Backward compatibility with existing code

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

**Usage:**
```bash
python run_tests.py                    # Run all tests with default verbosity
python run_tests.py --verbose          # Run tests with detailed pytest output
python run_tests.py -v                 # Same as --verbose
python run_tests.py --quiet            # Run tests with minimal output
python run_tests.py --help             # Show help and usage examples
```

**Options:**
- `--verbose`, `-v`: Enable verbose pytest output showing detailed test results
- `--quiet`, `-q`: Run tests with minimal output
- `--help`, `-h`: Show help message with usage examples and available options

**Test cases:**
- `test_17_times_23()`: Tests mathematical calculation (17 × 23 = 391)
- `test_reverse()`: Tests string reversal ("pineapple" → "elppaenip")
- `test_wordcount()`: Tests word counting ("to be or not to be" → 6 words)

**Features:**
- Comprehensive argument parsing with help documentation
- Flexible output verbosity control
- Automated validation of core agent functionality

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
