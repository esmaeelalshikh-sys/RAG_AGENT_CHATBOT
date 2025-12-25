import faiss
import pickle
import numpy as np

INDEX_PATH = "embeddings/faiss_index.bin"
PASSAGES_PATH = "embeddings/passages.pkl"


def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)
    return index


def load_passages():
    with open(PASSAGES_PATH, "rb") as f:
        passages = pickle.load(f)
    return passages