import os
import pickle
import numpy as np
import faiss
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMB_DIR = "embeddings"
INDEX_FILE = f"{EMB_DIR}/faiss_index.bin"
PASSAGES_FILE = f"{EMB_DIR}/passages.pkl"

# Load FAISS + passages
index = faiss.read_index(INDEX_FILE)

with open(PASSAGES_FILE, "rb") as f:
    passages = pickle.load(f)


def get_query_embedding(text: str):
    # GOOGLE GENAI NEW FORMAT
    for attempt in range(3):
        try:
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=[text]
            )

            # vector is inside: response.embeddings[0].values
            vector = np.array(response.embeddings[0].values, dtype="float32")
            return vector
        except Exception as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                wait_time = 30 * (2 ** attempt)
                print(f"Quota exceeded for embedding, retrying in {wait_time} seconds... (Attempt {attempt+1}/3)")
                time.sleep(wait_time)
            else:
                raise
    # Fallback: return a zero vector or handle gracefully
    print("Failed to get embedding due to quota limits. Using zero vector as fallback.")
    return np.zeros(768, dtype="float32")  # Assuming 768 dim for text-embedding-004


def retrieve_relevant_passages(query, top_k=5):
    q_emb = get_query_embedding(query).reshape(1, -1)
    distances, indices = index.search(q_emb, top_k)
    return [passages[i] for i in indices[0]]
