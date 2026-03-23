import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import (
    FAISS_INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL,
    TOP_K,
)

def load_index():
    return faiss.read_index(str(FAISS_INDEX_PATH))


def load_metadata():
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    query_embedding = model.encode([query], convert_to_numpy=True)
    query_embedding = query_embedding.astype("float32")
    return query_embedding

def search_index(query: str, top_k: int = TOP_K):
    index = load_index()
    metadata = load_metadata()
    model = SentenceTransformer(EMBEDDING_MODEL)

    query_embedding = embed_query(query, model)
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(metadata[idx])

    return results

if __name__ == "__main__":
    query = "Has Ismail worked with SQL?"
    results = search_index(query)

    print(f"\nQuery: {query}\n")
    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source: {result['source']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(result["text"])
        print("-" * 80)
