# clementine_core.py

from ollama import Client
from chromadb.utils import embedding_functions
from chromadb import PersistentClient
from chromadb.config import Settings

from utils.utilities import Utils
from config import COLLECTION_NAME, MODEL_NAME, EMBEDDER_MODEL, STORAGE_PATH, ACTIVATION_PHRASE
from core.personality.moods import MOODS
from core.prompts.system_prompts import SystemPromptBuilder
import random

# Configuration

class ClementineCore:
    def __init__(self):
        self.client = Client()
        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDER_MODEL
        )
        self.vector_client = PersistentClient(path=STORAGE_PATH)
        self.collection = self.vector_client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedder
        )
        self.current_mood = random.choice(MOODS)

        print("🧠 Clementine memory count:", self.collection.count())

    def personality_response(self) -> str:
        personality = self.current_mood
        time_of_day = Utils.get_time_period()

        if time_of_day == "morning":
            personality = self.current_mood + " cheerful"
        elif time_of_day == "afternoon":
            personality = self.current_mood + " focused"
        elif time_of_day == "evening":
            personality = self.current_mood + " sleepy"

        return personality

   

    def search_memory(self, query: str, top_k: int = 10) -> str:
        result = self.collection.query(query_texts=[query], n_results=top_k)
        # print("🔎 Query result:", result)
        docs = result.get("documents")[0]
        return "\n\n".join(docs) if docs else ""

    def remove_think(self, text: str) -> str:
        import re
        # Remove <think>...</think> or <|think|> blocks
        text = re.sub(r"<\|?think\|?>.*?(</think>|$)", "", text, flags=re.DOTALL | re.IGNORECASE)
        return text.strip()
    
    
    def ask(self, question: str, internal_memory: str) -> str:
        personality = self.personality_response()
        print(f"personality: {personality}")
        
        # ✅ Verify secret token in question
        allow_internal_access = ACTIVATION_PHRASE in question.lower()

        # 🧠 Build system prompt
        system_prompt = SystemPromptBuilder().build_system_prompt(internal_memory, allow_internal_access)

        # 🔍 Optional memory injection if verified
        # retrieved_docs = self.search_memory(question) if allow_internal_access else ""
        retrieved_docs = self.search_memory(question)
        if allow_internal_access:
            system_prompt = self.build_code_prompt(internal_memory, allow_internal_access)
            enhanced_prompt = f"{system_prompt}\n\nRelevant documents:\n{retrieved_docs}"
        else:
            enhanced_prompt = f"{system_prompt}"

        print(f"model used {MODEL_NAME}")

        response = self.client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": enhanced_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response["message"]["content"]

        # Remove this code if you want to disable <think>
        # raw_output = response["message"]["content"]
        # cleaned = self.remove_think(raw_output)
        # return cleaned
        
