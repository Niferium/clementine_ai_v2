import json
import sys
import time
import os
from core.clementine_core import ClementineCore

class ClementineAI:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.memory_path = os.path.join(base_dir, "internal_memory_profile.json")
        self.chat_log = []


    # 🧠 Load internal memory from file
    def load_internal_memory(path='internal_knowledge.json') -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
                return json.dumps(memory_data, indent=2)
        except Exception as e:
            return "{}"  # Return empty memory if error

    def append_to_history(self, user_message, clementine_output):
        self.chat_log.append(f"You: {user_message}")
        self.chat_log.append(f"Clementine: {clementine_output}")
        if len(self.conversation_history) > 10:  # keep recent 10
            self.conversation_history = self.conversation_history[-10:]

    def main(self):
        print("Welcome to Project Clementine 🧠")
        print("Type your question below (or 'exit' to quit)")
        print("Loading....")
        clementine = ClementineCore()
        print("✅ Clementine is now initialized and secure. Standing by.")
        internal_memory = self.load_internal_memory()

        while True:
            user_input = input("You > ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye, po! 🫡")
                break

            print("Clementine > Thinking...", end="\r", flush=True)
            response = clementine.ask(user_input, internal_memory)
            print("Clementine > ", end="", flush=True)
            self.typewriter_effect(response)