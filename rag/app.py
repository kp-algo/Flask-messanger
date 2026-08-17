import logging

from flask import Flask, request, jsonify

import retrieve
from generate import generate_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    retrieve.warm_up()
    logger.info("RAG service warmed up successfully.")
except Exception:
    logger.exception("Failed to warm up RAG service.")


@app.route("/health", methods=["GET"])
def health():
    if retrieve.is_ready():
        return jsonify({"status": "healthy"}), 200
    return jsonify({"status": "unhealthy"}), 503


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "query is required"}), 400

    try:
        context_chunks = retrieve.retrieve(query)
        answer = generate_response(query, context_chunks)
    except Exception:
        logger.exception("Error handling /chat request")
        return jsonify({"error": "internal error generating response"}), 500

    return jsonify({
        "response": answer,
        "sources": [
            {"source": chunk["source"], "excerpt": chunk["text"][:200]}
            for chunk in context_chunks
        ],
    })