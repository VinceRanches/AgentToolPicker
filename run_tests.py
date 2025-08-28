import subprocess
import pytest
import argparse
import sys

def run(q: str) -> str:
    out = subprocess.check_output(["python", "agent.py", q], text=True).strip()
    return out

def test_17_times_23():
    assert run("What's 17*23?") == "391"

def test_reverse():
    assert run("Reverse the word pineapple") == "elppaenip"

def test_wordcount():
    assert run('How many words are in: "to be or not to be"') == "6"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test Suite for AI Agent Tool Picker - Validates agent functionality with mathematical calculations, string operations, and word counting",
        epilog="Examples:\n"
               "  python run_tests.py              # Run all tests with default verbosity\n"
               "  python run_tests.py --verbose    # Run tests with detailed pytest output\n"
               "  python run_tests.py -v           # Same as --verbose\n"
               "  python run_tests.py --quiet      # Run tests with minimal output",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--verbose", "-v",
                       action="store_true",
                       help="Enable verbose pytest output showing detailed test results")
    parser.add_argument("--quiet", "-q",
                       action="store_true",
                       help="Run tests with minimal output")

    args = parser.parse_args()

    # Build pytest arguments based on command line options
    pytest_args = [__file__]

    if args.verbose:
        pytest_args.append("-v")
    elif args.quiet:
        pytest_args.append("-q")
    else:
        pytest_args.append("-v")  # Default to verbose for better user experience

    pytest.main(pytest_args)
