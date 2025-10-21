# clementine_memory_viewer.py
import local_chromadb
from collections import Counter
import argparse

# :blossom: Connect to ChromaDB
chroma_client = local_chromadb.PersistentClient(path="chromadb")
collection = chroma_client.get_collection("clementine-memory")
def list_all_entries():
    results = collection.get()
    for i, meta in enumerate(results["metadatas"]):
        type_label = meta.get("type", "no-type")
        print(f"{i+1}. ID: {results['ids'][i]} | Type: {type_label}")
def list_by_type(type_filter):
    results = collection.get()
    print(f"\n:open_file_folder: Listing entries of type: '{type_filter}'\n")
    found = False
    for i, meta in enumerate(results["metadatas"]):
        if meta.get("type") == type_filter:
            print(f":white_check_mark: {results['ids'][i]}")
            found = True
    if not found:
        print(":warning:  No entries found with that type.")
def preview_by_id(entry_id):
    results = collection.get(ids=[entry_id])
    docs = results.get("documents", [])
    if docs:
        print(f"\n:book: Preview of '{entry_id}':\n")
        print(docs[0][:1500])  # Limit to first 1500 characters
        print("\n:feather: ... (truncated)\n")
    else:
        print(":x: Entry not found.")
def show_type_counts():
    results = collection.get()
    types = [meta.get("type", "no-type") for meta in results["metadatas"]]
    counter = Counter(types)
    print("\n:bar_chart: Memory Types in Clementine's Brain:\n")
    for t, count in counter.items():
        print(f"• {t}: {count}")

def list_all_documents():
    results = collection.get()
    print(f"\n:books: Total documents found: {len(results['documents'])}\n")
    for i, doc in enumerate(results["documents"]):
        print(f"{i+1}. ID: {results['ids'][i]}")
        print(f"   Type: {results['metadatas'][i].get('type', 'no-type')}")
        print(f"   Preview: {doc[:100].strip().replace('', ' ')}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=":brain: Clementine's Memory Viewer")
    parser.add_argument("--all", action="store_true", help="List all entries in memory")
    parser.add_argument("--type", type=str, help="Filter entries by type")
    parser.add_argument("--preview", type=str, help="Preview a document by its ID")
    parser.add_argument("--count", action="store_true", help="Show count of each memory type")
    parser.add_argument("--documents", action="store_true", help="List all documents with preview")
    args = parser.parse_args()
    if args.all:
        list_all_entries()
    elif args.type:
        list_by_type(args.type)
    elif args.preview:
        preview_by_id(args.preview)
    elif args.count:
        show_type_counts()
    elif args.documents:
        list_all_documents()
    else:
        parser.print_help()






