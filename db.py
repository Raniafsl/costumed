import os

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

# Fixed color vocabulary used for filtering. Keep this list controlled —
# every look's colors must come from here, so filters stay meaningful.
COLOR_CATEGORIES = [
    "black", "white", "ivory", "red", "burgundy", "pink", "pastel-pink",
    "gold", "silver", "navy", "blue", "turquoise", "green", "mint",
    "khaki", "rust", "purple", "grey",
]

# Hex values used to render swatch strips/dots in the UI for each category.
COLOR_HEX = {
    "black": "#1a1a1a", "white": "#f5f5f0", "ivory": "#e9e2d0",
    "red": "#a3221f", "burgundy": "#5c1a25", "pink": "#d98a9c",
    "pastel-pink": "#f0c9d3", "gold": "#b08d57", "silver": "#c3c3c9",
    "navy": "#1f2a44", "blue": "#33587a", "turquoise": "#3f9c96",
    "green": "#3c5a3e", "mint": "#a8c9ab", "khaki": "#a89a6b",
    "rust": "#a4552e", "purple": "#5c3a5e", "grey": "#8a8a8a",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS films (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    director TEXT,
    genre TEXT
);

CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    film_id INTEGER NOT NULL REFERENCES films(id)
);

CREATE TABLE IF NOT EXISTS looks (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(id),
    scene_label TEXT,
    designer TEXT,
    era_decade TEXT,
    description TEXT,
    image_url TEXT,
    colors TEXT
);
"""


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Add it to a local .env file "
            "(see .env.example) or your host's environment variables."
        )
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    cur.close()
    conn.close()


def colors_to_str(color_list):
    return ",".join(color_list)


def colors_from_str(s):
    return [c for c in (s or "").split(",") if c]


def find_or_create_film(conn, title, year, director, genre):
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM films WHERE title = %s AND year = %s", (title, year)
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "INSERT INTO films (title, year, director, genre) VALUES (%s, %s, %s, %s) RETURNING id",
        (title, year, director, genre),
    )
    return cur.fetchone()["id"]


def find_or_create_character(conn, name, film_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM characters WHERE name = %s AND film_id = %s", (name, film_id)
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "INSERT INTO characters (name, film_id) VALUES (%s, %s) RETURNING id",
        (name, film_id),
    )
    return cur.fetchone()["id"]


def insert_look(conn, character_id, scene_label, designer, era_decade,
                 description, image_url, colors):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO looks
           (character_id, scene_label, designer, era_decade, description, image_url, colors)
           VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
        (character_id, scene_label, designer, era_decade, description,
         image_url, colors_to_str(colors)),
    )
    return cur.fetchone()["id"]


def get_all_looks(genre=None, decade=None, search=None):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT looks.*, characters.name AS character_name, characters.id AS character_id,
               films.title AS film_title, films.year AS film_year, films.genre AS film_genre
        FROM looks
        JOIN characters ON looks.character_id = characters.id
        JOIN films ON characters.film_id = films.id
        WHERE 1=1
    """
    params = []
    if genre:
        query += " AND films.genre = %s"
        params.append(genre)
    if decade:
        query += " AND looks.era_decade = %s"
        params.append(decade)
    if search:
        query += """ AND (
            films.title ILIKE %s OR characters.name ILIKE %s OR
            looks.scene_label ILIKE %s OR looks.designer ILIKE %s
        )"""
        needle = f"%{search}%"
        params.extend([needle, needle, needle, needle])
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r, colors=colors_from_str(r["colors"])) for r in rows]


def get_random_look_id():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM looks ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None


def get_look(look_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT looks.*, characters.name AS character_name, characters.id AS character_id,
                  films.title AS film_title, films.year AS film_year, films.genre AS film_genre
           FROM looks
           JOIN characters ON looks.character_id = characters.id
           JOIN films ON characters.film_id = films.id
           WHERE looks.id = %s""",
        (look_id,),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row, colors=colors_from_str(row["colors"]))


def get_other_looks_for_character(character_id, exclude_look_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT looks.*, characters.name AS character_name, films.title AS film_title
           FROM looks
           JOIN characters ON looks.character_id = characters.id
           JOIN films ON characters.film_id = films.id
           WHERE looks.character_id = %s AND looks.id != %s""",
        (character_id, exclude_look_id),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r, colors=colors_from_str(r["colors"])) for r in rows]


def get_distinct_genres():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT genre FROM films WHERE genre IS NOT NULL AND genre != '' ORDER BY genre"
    )
    rows = cur.fetchall()
    conn.close()
    return [r["genre"] for r in rows]


def get_distinct_decades():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT era_decade FROM looks WHERE era_decade IS NOT NULL AND era_decade != '' ORDER BY era_decade"
    )
    rows = cur.fetchall()
    conn.close()
    return [r["era_decade"] for r in rows]
