
import os
import sys
import time
from core.clementine_core import ClementineCore
from core.clementine_ai import ClementineAI

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
        clementine = ClementineAI()
        clementineCore = ClementineCore()
        print("✅ Clementine is now initialized and secure. Standing by.")
        internal_memory = clementine.load_internal_memory()

        while True:
            user_input = input("You > ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye, po! 🫡")
                break

            print("Clementine > Thinking...", end="\r", flush=True)
            response = clementineCore.ask(user_input, internal_memory)
            print("Clementine > ", end="", flush=True)
            typewriter_effect(response)

if __name__ == "__main__":
    main()