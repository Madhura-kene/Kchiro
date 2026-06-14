import sys
import os

# Set python path to find ollama_client
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.ollama_client import OllamaClient

def run_tests():
    client = OllamaClient()
    print(f"Initializing Ollama Client (connecting to {client.host}, model {client.model})...")
    
    test_prompts = [
        "Create a medieval iron sword with a leather grip.",
        "Build a round wooden table, width 140cm, height 80cm.",
        "Generate a small barrel of height 80cm and radius 30cm.",
        "Create a huge cube cargo crate of size 2 meters."
    ]
    
    print("\n--- Running Ollama Parsing Tests ---")
    for idx, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {idx}: Prompt: \"{prompt}\"")
        try:
            result = client.generate_json_spec(prompt)
            print("Extracted JSON Specification:")
            import pprint
            pprint.pprint(result)
        except Exception as e:
            print(f"Error executing test: {e}")

if __name__ == "__main__":
    run_tests()
