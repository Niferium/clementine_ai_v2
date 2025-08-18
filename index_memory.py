import os
from chromadb.utils import embedding_functions
from chromadb import PersistentClient
from config import STORAGE_PATH, COLLECTION_NAME, DOCS_FOLDER, EMBEDDER_MODEL
import sys

# 🌟 Step 1: Load embedding model once
embedder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDER_MODEL)

# 🌟 Step 2: Create Chroma client with embedder attached to collection
client = PersistentClient(path=STORAGE_PATH)  # ✅ New API

# Optionally clear old memory
if "--reset" in sys.argv:
    try:
        client.delete_collection("clementine-memory")
        print("🧼 Cleaned existing collection.")
    except:
        print("⚠️ Collection doesn't exist yet.")
        
collection = client.get_or_create_collection(
    name = COLLECTION_NAME,
    embedding_function=embedder
)

collections = client.list_collections()

print("📦 Collections in ChromaDB:")
for c in collections:
    print(f"• {c.name}")
    
# 🌟 Step 3: Scan documents folder

def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# def ingest_project(paths, collection):
#     print(f":mag: Scanning path: {paths}")   # show which folder
  
#     for root, _, files in os.walk(paths):
#             for file in files:
#                 if file.endswith((".kt", ".java", ".xml", ".gradle")):
#                     full_path = os.path.join(root, file)
#                     # DEBUG print
#                     print(f":white_check_mark: Found file: {full_path}")
#                     try:
#                         with open(full_path, "r", encoding="utf-8") as f:
#                             content = f.read()
#                         # you can also debug chunk sizes
#                         print(f"   ↳ Length: {len(content)} chars")
#                         chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
#                         print(f"   ↳ Split into {len(chunks)} chunks")
#                         for idx, chunk in enumerate(chunks):
#                             collection.add(
#                                 documents=[chunk],
#                                 metadatas=[{"file": full_path, "chunk": idx}],
#                                 ids=[f"{full_path}_{idx}"]
#                             )
#                     except Exception as e:
#                         print(f":warning: Error reading {full_path}: {e}")    
    
def ingest_project(paths, collection, recursive=False):
    for path in paths:
        print(f":open_file_folder: Scanning: {path}")
        if recursive:
            # normal recursive walk
            print(":Hello World")
            for root, _, files in os.walk(path):
                for file in files:
                    handle_file(root, file, collection)
        else:
            print(":Hello World2")
            # only current folder (no subdirs)
            print(os.listdir(path))
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    handle_file(path, file, collection)

def handle_file(root, file, collection):
    if file.endswith((".kt", ".java", ".xml", ".gradle")):
        full_path = os.path.join(root, file)
        print(f":white_check_mark: Found: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        for idx, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"file": full_path, "chunk": idx}],
                ids=[f"{full_path}_{idx}"]
            )
    print("Finished from android files")

docs_path = DOCS_FOLDER
ingest_project([docs_path], collection, recursive=False)
# filename = os.path.basename(DOCS_FOLDER)
# print(filename)

# for filename in os.listdir(docs_path):
#     file_path = os.path.join(docs_path, filename)
#     if not os.path.isfile(file_path):
#         continue

#     with open(file_path, 'r', encoding='utf-8',  errors='ignore') as f:
#         content = f.read()
#         print(f"Length: {len(content)}")
#         print(content[:500]) 
#         # chunks = content.split("\n\n")  # Split by paragraphs
#         chunks = split_text(content, chunk_size=500, overlap=100)
        
#         for i, chunk in enumerate(chunks):
#             if not chunk.strip():
#                 continue
#             collection.add(
#                 documents=[chunk],
#                 ids=[f"{filename}_{i}"]
#             )



print("✅ Clementine's memory has been indexed.")