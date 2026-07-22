# Costumed

A searchable archive of iconic film costumes, filterable by genre, era, and color — built to explore where cinema and fashion overlap.

## Why this exists

Most fashion databases are generic CRUD apps. This one is a curated archive: every costume look is tagged with a designer, era, and a fixed set of color categories, so you can browse an entire film's wardrobe, or flip it around and see every look across every film that shares a color palette — a "mood board" view built for visual discovery rather than raw data lookup.

## Features

- **Browse & filter** the full archive by genre, decade, or color
- **Character pages** that group multiple looks/scenes per character (a character can have several distinct costumes across a film)
- **Mood boards** — click any color swatch to see every look tagged with that color, across every film in the archive
- **Add a look** — a contribution form so the archive can grow over time

## Tech stack

- Flask (routing, templating)
- PostgreSQL (hosted on [Neon](https://neon.com)) via `psycopg2` (no ORM — direct SQL)
- Jinja2 templates, hand-written CSS (no framework)



Data written through the "Add a Look" form persists in the real database — it survives restarts and redeploys, unlike a SQLite file on ephemeral disk.

## Running the tests

The test suite needs its own database, separate from `DATABASE_URL`, so a test run can never truncate or clutter real archive data. 

## Project structure

```
costumed/
├── app.py            # Flask routes
├── db.py             # Postgres schema + query helpers, color vocabulary
├── seed.py           # populates the starter dataset
├── test_app.py        # pytest suite for routes and filtering
├── templates/        # Jinja2 templates
├── static/css/       # stylesheet
└── static/img/       # costume photography
```

## Data model

- **films** — title, year, director, genre
- **characters** — name, linked to a film
- **looks** — the core entity: one row per costume/scene, linked to a character, with designer, era, description, and a set of color tags

A character can have multiple `looks` (e.g. Elizabeth Lavenza in *Frankenstein* has four distinct costume moments), which is what makes the "more from this character" and mood-board features possible.

## Next steps / ideas for extending

- Add user accounts so people can submit and favorite looks
- Add image uploads instead of relying on external image URLs or manually-added files
- Basic spam protection on the contribution form now that submissions are permanent
