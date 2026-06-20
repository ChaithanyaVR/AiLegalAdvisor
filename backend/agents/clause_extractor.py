import requests

OLLAMA_URL = \
"http://localhost:11434/api/generate"

def extract_clauses(text):

    prompt=f"""
You are a legal clause extractor.

Extract ONLY:

1. Payment Clause
2. Liability Clause
3. Termination Clause
4. Confidentiality Clause
5. Jurisdiction Clause

Return STRICT JSON.

Contract:

{text[:5000]}
"""

    response=requests.post(

        OLLAMA_URL,

        json={

            "model":"llama3",

            "prompt":prompt,

            "stream":False
        }
    )

    data=response.json()

    return data["response"]