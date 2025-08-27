import subprocess
import pytest

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
    pytest.main([__file__, "-v"])
