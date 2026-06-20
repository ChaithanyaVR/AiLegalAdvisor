from flask import (

    Blueprint,
    jsonify

)

from psycopg2.extras import (
    RealDictCursor
)

from db import (

    get_db,
    release_db

)

analysis_bp = Blueprint(

    "analysis_routes",

    __name__

)

@analysis_bp.route(

    "/analyses",

    methods=["GET"]

)
def get_analyses():

    conn = None

    try:

        conn = get_db()

        with conn.cursor(

            cursor_factory=
            RealDictCursor

        ) as cur:

            cur.execute("""

                SELECT *

                FROM analysis_results

                ORDER BY
                created_at DESC

            """)

            results = \
                cur.fetchall()

            return jsonify(
                results
            )

    finally:

        if conn:

            release_db(conn)