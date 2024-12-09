import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def fetch_all(conn, query, values=()):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(query, values)
        return cur.fetchall()


def add_url_to_db(url):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
            conn.commit()


def get_url_by_name(url):
    with psycopg2.connect(DATABASE_URL) as conn:
        query = "SELECT * FROM urls WHERE name = %s"
        return fetch_all(conn, query, (url,))


def get_url_by_id(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        query = "SELECT * FROM urls WHERE id = %s"
        return fetch_all(conn, query, (url_id,))


def add_check_to_db(url_id, status_code, page_data):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description) "
                "VALUES (%s, %s, %s, %s, %s)",
                (url_id, status_code,
                 page_data['h1'], page_data['title'], page_data['description']),
            )
            conn.commit()


def get_urls_with_latest_check():
    with psycopg2.connect(DATABASE_URL) as conn:
        query = (
            "SELECT urls.id, urls.name, "
            "COALESCE(url_checks.status_code::text, '') as status_code, "
            "COALESCE(MAX(url_checks.created_at)::text, '') as latest_check "
            "FROM urls "
            "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
            "GROUP BY urls.id, url_checks.status_code "
            "ORDER BY urls.id DESC"
        )
        return fetch_all(conn, query)


def get_checks_desc(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        query = (
            "SELECT id, status_code, COALESCE(h1, '') as h1, "
            "COALESCE(title, '') as title, COALESCE(description, '') as description, "
            "created_at::text FROM url_checks WHERE url_id = %s ORDER BY id DESC"
        )
        return fetch_all(conn, query, (url_id,))
