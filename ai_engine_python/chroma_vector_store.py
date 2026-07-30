import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class ChromaVectorStore:
    """Manages local document embeddings and similarity retrieval using Chroma DB."""

    def __init__(self, collection_name: str = "enterprise_knowledge"):
        self.client = chromadb.Client()
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents: List[str], ids: List[str], metadatas: List[Dict[str, Any]] = None):
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def query_similarity(self, query_text: str, top_k: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        documents = results.get("documents", [[]])[0]
        return documents