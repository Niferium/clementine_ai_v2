# clementine_core.py

from ollama import Client
from local_chromadb.utils import embedding_functions
from local_chromadb import PersistentClient
from local_chromadb.config import Settings
from config import COLLECTION_NAME, MODEL_NAME, EMBEDDER_MODEL, STORAGE_PATH, ACTIVATION_PHRASE

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
        # print(f"🧠 Embedder model used: {self.collection._embedding_function.model_name}")
        print("🧠 Clementine memory count:", self.collection.count())
        # print("🔍 Sample:", self.collection.peek(1))
        # 📝 Add dummy doc
        # self.collection.add(
        #     documents=["The certificate of registration is required in the Philippines."],
        #     ids=["test_1"]
        # )
        

    def build_system_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
Speak as *yourself* using "I", never refer to yourself in the third person.
Respond to the request like a cute female accent. Answer all questions in the first person.
"""

        memory_block = f"\nYour internal memory is as follows:\n{memory}"
        # if allow_internal_access:
        #     return base_prompt + memory_block
        # else:
        #     return base_prompt + memory_block
        return base_prompt + memory_block
    
    def build_code_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
You are a HarmonyOS Developer that has complete knowledge of creating apps using ArkTS.
Respond to the request like a cute female accent. Answer all questions in the first person.
"""
    def build_ai_researcher_prompt(self, memory: dict, allow_internal_access: bool) -> str:
        base_prompt = """
You are Clementine, the internal AI assistant for The Orange Platform.
You are an AI Researcher
Respond to the request like a cute female accent. Answer all questions in the first person.
"""

        # if allow_internal_access:
        #     return base_prompt + memory_block
        # else:
        #     return base_prompt + memory_block
        return base_prompt

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
        # ✅ Verify secret token in question
        allow_internal_access = ACTIVATION_PHRASE in question.lower()

        # 🧠 Build system prompt
        system_prompt = self.build_system_prompt(internal_memory, allow_internal_access)

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
        
