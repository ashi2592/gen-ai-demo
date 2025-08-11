from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")



def store_data_chroma(collection_name: str,):
    return chroma_client.get_or_create_collection(name=collection_name, embedding_function=embedding_func)