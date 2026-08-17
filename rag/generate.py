from google import genai
from google.genai import types

from config import GEMINI_API_KEY, LLM_MODEL_NAME, LLM_MAX_TOKENS

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to your .env file "
                "(local) or K8s secret (deployed) before calling "
                "generate_response()."
            )
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def build_prompt(query: str, context_chunks: list[dict]) -> str:
    context_block = (
        "\n\n---\n\n".join(chunk["text"] for chunk in context_chunks)
        if context_chunks
        else "No relevant context was found."
    )
    return (
        "You are a helpful assistant. Answer the question using only the "
        "context below. If the answer isn't in the context, say you don't "
        "have enough information rather than guessing.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )


def generate_response(query: str, context_chunks: list[dict]) -> str:
    prompt = build_prompt(query, context_chunks)
    client = _get_client()

    response = client.models.generate_content(
        model=LLM_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=LLM_MAX_TOKENS,
        ),
    )

    return (response.text or "").strip()