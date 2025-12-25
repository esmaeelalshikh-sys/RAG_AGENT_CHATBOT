# rag/preprocess.py (الإصدار المصحح)

import os
import faiss
import pickle
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
import google.genai # تم تغيير الاستيراد ليصبح أكثر دقة
import time

load_dotenv()

DATA_PATH = "data/Syrian_Universities_IT_KB_Bilingual.txt"
EMB_DIR = "embeddings"
INDEX_FILE = f"{EMB_DIR}/faiss_index.bin"
PASSAGES_FILE = f"{EMB_DIR}/passages.pkl"

# تهيئة Gemini Client مباشرةً باستخدام الكلاس
client = google.genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class SimpleAgent:
    def __init__(self):
        self.model = "gemini-2.0-flash"
        
def load_text():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=350):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# دالة التضمين تم تعديلها لاستخدام كائن client
def get_embedding(text):
    for attempt in range(3):
        try:
            result = client.models.embed_content( # الوصول إلى embed_content عبر client.models
                model="text-embedding-004",
                contents=[text] # يجب أن تكون قائمة (list) حتى لو كانت تحتوي على قطعة واحدة
            )
            # العودة بقيم التضمين الصحيحة من كائن الرد
            return result.embeddings[0].values
        except Exception as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                wait_time = 30 * (2 ** attempt)
                print(f"Quota exceeded for embedding, retrying in {wait_time} seconds... (Attempt {attempt+1}/3)")
                time.sleep(wait_time)
            else:
                raise
    print("Failed to get embedding due to quota limits. Skipping this chunk.")
    return [0.0] * 768  # Return zero vector 

def build_faiss(chunks):
    os.makedirs(EMB_DIR, exist_ok=True)

    print("🔄 Generating embeddings...")
    embeddings = [get_embedding(chunk) for chunk in tqdm(chunks)]

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, INDEX_FILE)
    print("✅ FAISS index saved.")

    with open(PASSAGES_FILE, "wb") as f:
        pickle.dump(chunks, f)
    print("✅ Passages saved.")

    print("🎉 Preprocessing complete!")

if __name__ == "__main__":
    print("📘 Loading knowledge base...")
    text = load_text()

    print("✂ Splitting into chunks...")
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")

    print("⚙ Building vector index...")
    build_faiss(chunks)