import json
import sys
import argparse
from tools import TOOLS
from policy import call_llm
from io_models import FinalAnswer

def run_agent(question: str, verbose: bool = False):
    if verbose:
        print(f"🤖 Starting agent with question: {question}")
        print("=" * 50)

    history = [{"role": "user", "content": question}]

    for step in range(3):
        if verbose:
            print(f"\n📍 Step {step + 1}:")
            print(f"Current history length: {len(history)} messages")

        decision = call_llm(history)

        if isinstance(decision, FinalAnswer):
            if verbose:
                print(f"✅ Final answer received: {decision.content}")
            else:
                print(decision.content)
            return

        if verbose:
            print(f"🔧 Tool call: {decision.tool}")
            print(f"📝 Arguments: {json.dumps(decision.args, indent=2)}")

        tool = TOOLS.get(decision.tool)
        if not tool:
            obs = {"error": "Unknown tool"}
            if verbose:
                print(f"❌ Error: Unknown tool '{decision.tool}'")
        else:
            try:
                obs = tool.call(decision.args)
                if verbose:
                    print(f"🔍 Tool result: {json.dumps(obs, indent=2)}")
            except Exception as e:
                obs = {"error": str(e)}
                if verbose:
                    print(f"❌ Tool execution error: {str(e)}")

        history.append({"role": "assistant", "content": json.dumps({"tool": decision.tool, "args": decision.args})})
        history.append({"role": "user", "content": json.dumps(obs)})

        # Give the LLM a chance to provide a final answer based on the tool result
        decision = call_llm(history)

        if isinstance(decision, FinalAnswer):
            if verbose:
                print(f"✅ Final answer received: {decision.content}")
            else:
                print(decision.content)
            return

    if verbose:
        print("\n⚠️ Maximum steps exceeded")
    print("Exceeded max steps.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI agent with tool selection capabilities")
    parser.add_argument("question", help="The question to ask the agent")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output showing the agent's decision process")

    args = parser.parse_args()

    if not args.question:
        print("Usage: python agent.py 'question' [--verbose]")
        sys.exit(1)

    run_agent(args.question, args.verbose)
