import os
import hashlib
import pickle
from typing import Dict
from utils.llm_model import llm
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage

# ---- Config ----
embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="global_knowledge", embedding_function=embedding_func)


# ---- Cache Setup ----
CACHE_PATH = "cache/query_cache.pkl"
os.makedirs("cache", exist_ok=True)
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "rb") as f:
        QUERY_CACHE: Dict[str, str] = pickle.load(f)
else:
    QUERY_CACHE = {}

def save_cache():
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(QUERY_CACHE, f)

# ---- Helper: Hash-based key for queries ----
def hash_query(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

# ---- Helper: Document chunking for better granularity ----
def chunk_text(text: str, max_length: int = 300):
    words = text.split()
    return [" ".join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

# ---- Add new docs periodically ----
def ingest_documents(docs):
    chunks = []
    ids = []
    for i, d in enumerate(docs):
        for j, chunk in enumerate(chunk_text(d["text"])):
            chunks.append(chunk)
            ids.append(f"{d['id']}_{j}")
    collection.add(documents=chunks, ids=ids)

# Example usage (can be run as a scheduled job)
# ingest_documents([{"id": "wiki1", "text": "LangChain is a Python framework..."}])

# ---- Retrieve with fallback ----
def retrieve_context(query: str) -> str:
    results = collection.query(query_texts=[query], n_results=3)
    return "\n".join(results["documents"][0]) if results["documents"] else ""

# ---- Main chat agent handler ----
def chat_agent_handler(input_data):
    user_input = input_data["input"]
    user_id = input_data.get("user_id", "global")

    cache_key = hash_query(user_input)
    if cache_key in QUERY_CACHE:
        return QUERY_CACHE[cache_key]

    context = retrieve_context(user_input)

    if context:
        prompt = f"""
        You are a helpful assistant. Use the following global context to answer the question.

        Context:
        {context}

        User: {user_input}
        Assistant:
        """
    else:
        prompt = f"""
        You are a helpful assistant. Answer the following user query using your knowledge.

        User: {user_input}
        Assistant:
        """

    response = llm.invoke([HumanMessage(content=prompt)])
    parsed_response = response.content.strip()
    QUERY_CACHE[cache_key] = parsed_response
    save_cache()
    return parsed_response

# Exportable agent
chat_agent = RunnableLambda(chat_agent_handler)