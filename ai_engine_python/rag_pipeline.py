from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from slm_orchestrator import AzureFoundrySLM
from chroma_vector_store import ChromaVectorStore

app = FastAPI(title="Azure SLM RAG Microservice")

slm_engine = AzureFoundrySLM()
vector_store = ChromaVectorStore()

class QueryRequest(BaseModel):
    prompt: str
    top_k: int = 3

class IngestRequest(BaseModel):
    documents: list
    ids: list

@app.post("/api/ingest")
async def ingest_docs(request: IngestRequest):
    try:
        vector_store.add_documents(documents=request.documents, ids=request.ids)
        return {"status": "success", "count": len(request.documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag")
async def process_rag(request: QueryRequest):
    try:
        context_chunks = vector_store.query_similarity(request.prompt, top_k=request.top_k)
        if not context_chunks:
            return {"answer": "No relevant context found.", "tokens_used": 0}

        combined_context = "\n---\n".join(context_chunks)
        result = slm_engine.generate_response(context=combined_context, prompt=request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))