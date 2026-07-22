# Costumed

A searchable archive of iconic film costumes, filterable by genre, era, and color — built to explore where cinema and fashion overlap.

## Why this exists

Most "portfolio project" databases are generic CRUD apps. This one is a curated archive: every costume look is tagged with a designer, era, and a fixed set of color categories, so you can browse an entire film's wardrobe, or flip it around and see every look across every film that shares a color palette — a "mood board" view built for visual discovery rather than raw data lookup.

## Features

- **Browse & filter** the full archive by genre, decade, or color
- **Character pages** that group multiple looks/scenes per character (a character can have several distinct costumes across a film)
- **Mood boards** — click any color swatch to see every look tagged with that color, across every film in the archive
- **Add a look** — a contribution form so the archive can grow over time

## Tech stack

- Flask (routing, templating)
- SQLite via Python's built-in `sqlite3` module (no ORM — direct SQL)
- Jinja2 templates, hand-written CSS (no framework)

## Running it locally

```bash
pip install -r requirements.txt
python seed.py      # populates costumed.db with the starter dataset
python app.py        # starts the dev server at http://127.0.0.1:5000
```

## Running the tests

```bash
pytest test_app.py -v
```

## Project structure

```
costumed/
├── app.py            # Flask routes
├── db.py             # sqlite3 schema + query helpers, color vocabulary
├── seed.py           # populates the starter dataset
├── test_app.py        # pytest suite for routes and filtering
├── templates/        # Jinja2 templates
└── static/css/       # stylesheet
```

## Data model

- **films** — title, year, director, genre
- **characters** — name, linked to a film
- **looks** — the core entity: one row per costume/scene, linked to a character, with designer, era, description, and a set of color tags

A character can have multiple `looks` (e.g. Elizabeth Lavenza in *Frankenstein* has four distinct costume moments), which is what makes the "more from this character" and mood-board features possible.

## Next steps / ideas for extending

- Expand the dataset beyond the current ~15 looks
- Add user accounts so people can submit and favorite looks
- Add image uploads instead of relying on external image URLs
