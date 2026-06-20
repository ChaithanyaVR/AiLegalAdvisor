from flask import Blueprint, request, jsonify
import os
import json

from db import get_db

from services.pdf_service import (
    extract_pdf_text
)

from agents.clause_extractor import (
    extract_clauses
)

from services.embedding_service import (
    generate_embedding
)

from services.chunk_service import (
    chunk_text
)

upload_bp = Blueprint(
    "upload_routes",
    __name__
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@upload_bp.route(
    "/upload",
    methods=["POST"]
)
def upload_document():

    print(
        "\n========== UPLOAD ROUTE HIT =========="
    )

    if "file" not in request.files:

        return jsonify({
            "error":"No file uploaded"
        }),400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "error":"Empty filename"
        }),400

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    print(
        "STEP 1: File saved ->",
        filepath
    )

    conn = None

    try:

        print(
            "\nSTEP 2: Starting PDF extraction..."
        )

        extracted_text = \
            extract_pdf_text(
                filepath
            )

        print(
            "STEP 3: PDF extraction completed"
        )

        print(
            "\nSTEP 4: Starting clause extraction..."
        )

        clauses = \
            extract_clauses(
                extracted_text
            )

        print(
            "STEP 5: Clause extraction completed"
        )

        print(
            "\nSTEP 6: Saving contract..."
        )

        conn = get_db()

        with conn.cursor() as cur:

            cur.execute("""

                INSERT INTO
                analysis_results

                (

                    filename,

                    extracted_text,

                    clauses

                )

                VALUES

                (

                    %s,

                    %s,

                    %s

                )

                RETURNING id

            """,

            (

                file.filename,

                extracted_text,

                json.dumps(
                    clauses
                )

            ))

            contract_id = \
                cur.fetchone()[0]

            print(
                f"Contract ID: {contract_id}"
            )

            print(
                "\nSTEP 7: Creating chunks..."
            )

            chunks = \
                chunk_text(
                    extracted_text
                )

            print(
                f"Created {len(chunks)} chunks"
            )

            print(
                "\nSTEP 8: Saving chunks..."
            )

            for index, chunk in enumerate(chunks):

                print(
                    f"Saving chunk {index + 1}"
                )

                embedding = \
                    generate_embedding(
                        chunk
                    )

                cur.execute("""

                    INSERT INTO
                    contract_chunks

                    (

                        contract_id,

                        chunk_text,

                        embedding

                    )

                    VALUES

                    (

                        %s,

                        %s,

                        %s

                    )

                """,

                (

                    contract_id,

                    chunk,

                    json.dumps(
                        embedding
                    )

                ))

            conn.commit()

            print(
                "STEP 9: Contract + Chunks Stored"
            )

        return jsonify({

            "contract_id":
            contract_id,

            "message":
            "Analysis complete",

            "filename":
            file.filename,

            "extracted_text":
            extracted_text,

            "clauses":
            clauses

        })

    except Exception as e:

        print(
            "\nERROR:"
        )

        print(
            str(e)
        )

        if conn:

            conn.rollback()

        return jsonify({

            "error":
            str(e)

        }),500

    finally:

        if conn:

            conn.close()