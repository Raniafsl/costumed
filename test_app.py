import os
import pytest
import db as db_module
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Point the app at a throwaway sqlite file for each test."""
    test_db_path = tmp_path / "test_costumed.db"
    monkeypatch.setattr(db_module, "DB_PATH", str(test_db_path))
    db_module.init_db()

    conn = db_module.get_connection()
    film_id = db_module.find_or_create_film(conn, "Test Film", 2020, "Test Director", "horror")
    char_id = db_module.find_or_create_character(conn, "Test Character", film_id)
    db_module.insert_look(
        conn, char_id, "Test Scene", "Test Designer", "1990s",
        "A test description", "", ["black", "red"],
    )
    conn.commit()
    conn.close()

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Test Character" in resp.data


def test_genre_filter(client):
    resp = client.get("/?genre=horror")
    assert b"Test Character" in resp.data
    resp_empty = client.get("/?genre=sci-fi")
    assert b"Test Character" not in resp_empty.data


def test_color_filter_mood_board(client):
    resp = client.get("/mood/red")
    assert resp.status_code == 200
    assert b"Test Character" in resp.data
    resp_empty = client.get("/mood/mint")
    assert b"Test Character" not in resp_empty.data


def test_look_detail_page(client):
    resp = client.get("/look/1")
    assert resp.status_code == 200
    assert b"Test Scene" in resp.data
    assert b"Test Designer" in resp.data


def test_look_detail_404(client):
    resp = client.get("/look/999")
    assert resp.status_code == 404


def test_add_look_form_get(client):
    resp = client.get("/add")
    assert resp.status_code == 200
    assert b"Add a look to the archive" in resp.data


def test_add_look_form_post_creates_entry(client):
    resp = client.post("/add", data={
        "film_title": "New Film",
        "film_year": "2021",
        "director": "New Director",
        "genre": "fashion-world",
        "character_name": "New Character",
        "scene_label": "New Scene",
        "designer": "New Designer",
        "era_decade": "2020s",
        "description": "New description",
        "image_url": "",
        "colors": ["gold", "ivory"],
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"New Character" in resp.data


def test_multiple_looks_same_character_show_as_related(client):
    conn = db_module.get_connection()
    char_row = conn.execute(
        "SELECT id FROM characters WHERE name = 'Test Character'"
    ).fetchone()
    db_module.insert_look(
        conn, char_row["id"], "Second Scene", "Test Designer", "1990s",
        "Another look for the same character", "", ["ivory"],
    )
    conn.commit()
    conn.close()

    resp = client.get("/look/1")
    assert b"Second Scene" in resp.data
