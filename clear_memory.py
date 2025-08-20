# clear_memory.py

from chromadb import PersistentClient
from config import STORAGE_PATH, COLLECTION_NAME

# Path to Clementine's stored memory
def clear_memory():
    client = PersistentClient(path=STORAGE_PATH)
    collections = client.list_collections()

    if any(c.name == COLLECTION_NAME for c in collections):
        client.delete_collection(COLLECTION_NAME)
        print(f"🧼 Successfully cleared '{COLLECTION_NAME}' collection.")
    else:
        print(f"⚠️ Collection '{COLLECTION_NAME}' not found. Nothing to clear.")

if __name__ == "__main__":
    confirm = input(f"❗ Are you sure you want to delete '{COLLECTION_NAME}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        clear_memory()
    else:
        print("🛑 Cancelled. Clementine's memory is safe.")