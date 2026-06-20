from flask import (
    Blueprint,
    request,
    jsonify
)

from psycopg2.extras import (
    RealDictCursor
)

from db import get_db

from agents.rag_chatbot import (
    ask_contract
)

chat_bp = Blueprint(
    "chat_routes",
    __name__
)


@chat_bp.route(
    "/chat",
    methods=["POST"]
)
def chat():

    conn = None

    try:

        data = request.get_json()

        contract_id = \
            data["contract_id"]

        question = \
            data["question"]

        conn = get_db()

        with conn.cursor(

            cursor_factory=
            RealDictCursor

        ) as cur:

            cur.execute("""

                SELECT

                    chunk_text,

                    embedding

                FROM

                    contract_chunks

                WHERE

                    contract_id = %s

            """,

            (

                contract_id,

            ))

            chunks = \
                cur.fetchall()

        answer = \
            ask_contract(

                question,

                chunks

            )

        return jsonify({

            "answer":
            answer

        })

    except Exception as e:

        print(
            "CHAT ERROR:"
        )

        print(
            str(e)
        )

        return jsonify({

            "error":
            str(e)

        }),500

    finally:

        if conn:

            conn.close()