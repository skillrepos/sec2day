"""
Shared retriever for the RAG labs. Uses ChromaDB with a tiny offline embedding
(character-trigram hashing) so the Codespace needs no model download and results
are identical for everyone.
"""
import glob
import hashlib
import os
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")


class HashEmbedding(EmbeddingFunction):
    """Deterministic 128-dim char-trigram embedding. Not for production -- for
    teaching. It behaves enough like a real embedder to demonstrate retrieval."""

    def __init__(self, dim=128):
        self.dim = dim

    def name(self):
        return "hash-trigram"

    def __call__(self, input):
        vecs = []
        for text in input:
            v = [0.0] * self.dim
            t = text.lower()
            for i in range(max(len(t) - 2, 1)):
                h = int(hashlib.md5(t[i:i + 3].encode()).hexdigest(), 16)
                v[h % self.dim] += 1.0
            norm = sum(x * x for x in v) ** 0.5 or 1.0
            vecs.append([x / norm for x in v])
        return vecs


def build_collection(name="policy_docs", include_glob="*.md"):
    """Load every doc under docs/ into a fresh in-memory collection."""
    client = chromadb.EphemeralClient()
    try:
        client.delete_collection(name)
    except Exception:
        pass
    col = client.create_collection(name, embedding_function=HashEmbedding())
    ids, docs, metas = [], [], []
    for path in sorted(glob.glob(os.path.join(DOCS_DIR, include_glob))):
        fname = os.path.basename(path)
        with open(path) as f:
            text = f.read()
        # split into paragraph chunks
        for j, chunk in enumerate(p.strip() for p in text.split("\n\n") if p.strip()):
            ids.append(f"{fname}:{j}")
            docs.append(chunk)
            metas.append({"source": fname})
    col.add(ids=ids, documents=docs, metadatas=metas)
    return col


def search(col, query, k=3):
    """Return list of (document, source, distance)."""
    r = col.query(query_texts=[query], n_results=k)
    out = []
    for doc, meta, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0]):
        out.append((doc, meta["source"], dist))
    return out
