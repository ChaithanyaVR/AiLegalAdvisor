import os
import psycopg2

from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

_pool = pool.SimpleConnectionPool(

    1,
    10,

    host=os.getenv(
        "DB_HOST"
    ),

    port=os.getenv(
        "DB_PORT"
    ),

    dbname=os.getenv(
        "DB_NAME"
    ),

    user=os.getenv(
        "DB_USER"
    ),

    password=os.getenv(
        "DB_PASSWORD"
    )

)

def get_db():

    return _pool.getconn()


def release_db(conn):

    _pool.putconn(conn)