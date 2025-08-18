# internal_ai_wrapper.py

from clementine_core import ClementineCore
import json
import sys
import time

# 🧠 Load internal memory from file
def load_internal_memory(path='internal_knowledge.json') -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            memory_data = json.load(f)
            return json.dumps(memory_data, indent=2)
    except Exception as e:
        return "{}"  # Return empty memory if error

def typewriter_effect(text: str, delay: float = 0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Final newline


def main():
    print("Welcome to Project Clementine 🧠")
    print("Type your question below (or 'exit' to quit)")
    print("Loading....")
    clementine = ClementineCore()
    print("✅ Clementine is now initialized and secure. Standing by.")
    internal_memory = load_internal_memory()

    while True:
        user_input = input("You > ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye, po! 🫡")
            break

        print("Clementine > Thinking...", end="\r", flush=True)
        response = clementine.ask(user_input, internal_memory)
        print("Clementine > ", end="", flush=True)
        typewriter_effect(response)


if __name__ == '__main__':
    main()
