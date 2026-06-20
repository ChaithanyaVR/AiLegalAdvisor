import json

from db import get_db

def save_analysis(
    filename,
    extracted_text,
    clauses
):

    with get_db() as conn:

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
                (%s,%s,%s)

                RETURNING id;

            """,

            (

                filename,

                extracted_text,

                json.dumps(
                    clauses
                )

            ))

            analysis_id = \
                cur.fetchone()[0]

            conn.commit()

            return analysis_id