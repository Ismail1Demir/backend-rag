from pathlib import Path
from typing import List, Dict
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import (
    DATA_DIR,
    VECTOR_STORE_DIR,
    FAISS_INDEX_PATH,
    METADATA_PATH,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

def read_markdown_files(data_dir: Path) -> List[Dict]:
    documents = []
    for file_path in data_dir.glob("*.md"):
        content = file_path.read_text(encoding="utf-8").strip()
        
        if not content:
            continue
        documents.append(
            {
                "source": file_path.name,
                "content": content
            }
        )
    return documents

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)
        if end >= text_length:
            break
        start = end - overlap
    return chunks

def build_chunk_records(documents: List[Dict]) -> List[Dict]:
    records = []

    for doc in documents:
        chunks = chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            records.append({
                "id": len(records),
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk,
            })

    return records

def create_embeddings(texts: List[str], model_name: str) -> np.ndarray:
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )
    embeddings = embeddings.astype("float32")
    return embeddings

def save_faiss_index(embeddings: np.ndarray, output_path: Path) -> faiss.Index:
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, str(output_path))
    return index

def save_metadata(records: List[Dict], output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def main() -> None:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    documents = read_markdown_files(DATA_DIR)
    if not documents:
        raise ValueError(f"No markdown files found in {DATA_DIR}")

    records = build_chunk_records(documents)
    texts = [record["text"] for record in records]

    embeddings = create_embeddings(texts, EMBEDDING_MODEL)
    save_faiss_index(embeddings, FAISS_INDEX_PATH)
    save_metadata(records, METADATA_PATH)

    print("Ingestion complete.")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(records)}")
    print(f"Index saved to: {FAISS_INDEX_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    main()