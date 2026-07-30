import os
from azure.ai.inference import ModelClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Any

class AzureFoundrySLM:
    """Orchestrates Small Language Models (Phi-3) via Azure AI Foundry endpoints."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT", "https://your-foundry-endpoint.inference.ai.azure.com")
        self.api_key = os.getenv("AZURE_AI_FOUNDRY_KEY", "mock-key")
        self.client = ModelClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )

    def generate_response(self, context: str, prompt: str) -> Dict[str, Any]:
        system_instructions = (
            "You are a precise AI assistant. Synthesize an answer based ONLY on the provided context. "
            "If the context does not contain the answer, state 'Data unavailable in context.'"
        )
        
        user_content = f"Context:\n{context}\n\nQuestion: {prompt}"

        response = self.client.complete(
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_content}
            ],
            model="phi-3-mini-4k-instruct",
            temperature=0.1,
            max_tokens=400
        )

        return {
            "answer": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "model": "phi-3-mini-4k-instruct"
        }