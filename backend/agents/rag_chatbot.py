import json
import requests
import numpy as np

from services.embedding_service import (
    generate_embedding
)

OLLAMA_URL = \
    "http://localhost:11434/api/generate"


def cosine_similarity(

    a,

    b

):

    a = np.array(a)

    b = np.array(b)

    return np.dot(

        a,

        b

    ) / (

        np.linalg.norm(a)

        *

        np.linalg.norm(b)

    )


def ask_contract(

    question,

    chunks

):

    query_embedding = \
        generate_embedding(
            question
        )

    scored = []

    for chunk in chunks:

        similarity = \
            cosine_similarity(

                query_embedding,

                chunk["embedding"]

            )

        scored.append({

            "text":
            chunk["chunk_text"],

            "score":
            similarity

        })

    top_chunks = sorted(

        scored,

        key=lambda x:
        x["score"],

        reverse=True

    )[:3]

    context = "\n".join(

        [

            chunk["text"]

            for chunk
            in top_chunks

        ]

    )

    prompt = f"""

Answer only using
the contract.

Context:

{context}

Question:

{question}

"""

    response = requests.post(

        OLLAMA_URL,

        json={

            "model":
            "llama3",

            "prompt":
            prompt,

            "stream":
            False

        }

    )

    return response.json()[
        "response"
    ]