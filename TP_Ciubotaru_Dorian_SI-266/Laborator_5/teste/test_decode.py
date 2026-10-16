import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arsenal.forensics.decode import desfa

def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"
    print("Testul pentru base64 a trecut cu succes!")

if __name__ == "__main__":
    test_base64()
