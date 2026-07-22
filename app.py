from flask import Flask, render_template, request, redirect, url_for
import os
import random
import db

app = Flask(__name__)
app.jinja_env.globals["color_hex"] = lambda tag: db.COLOR_HEX.get(tag, "#999999")


def gradient_for(colors):
    """A little swatch-card gradient built from a look's own color tags,
    used when no photograph is on file — keeps the archive feeling curated
    instead of broken, and keeps us from guessing at film-still URLs."""
    hexes = [db.COLOR_HEX.get(c, "#2a2c3d") for c in colors] or ["#2a2c3d", "#1c1e2b"]
    if len(hexes) == 1:
        hexes = hexes * 2
    return "linear-gradient(135deg, " + ", ".join(hexes) + ")"


app.jinja_env.globals["gradient_for"] = gradient_for


@app.route("/")
def index():
    """Browse page — supports filtering by color, material, genre, and decade via query params."""
    color = request.args.get("color", "")
    material = request.args.get("material", "")
    genre = request.args.get("genre", "")
    decade = request.args.get("decade", "")
    search = request.args.get("q", "").strip()

    looks = db.get_all_looks(genre=genre or None, decade=decade or None, search=search or None)

    if color:
        looks = [l for l in looks if color in l["colors"]]
    if material:
        looks = [l for l in looks if material in l["materials"]]

    any_filter = color or material or genre or decade or search
    featured = random.choice(looks) if looks and not any_filter else None

    return render_template(
        "index.html",
        looks=looks,
        featured=featured,
        colors=db.COLOR_CATEGORIES,
        materials=db.MATERIAL_CATEGORIES,
        genres=db.get_distinct_genres(),
        decades=db.get_distinct_decades(),
        selected_color=color,
        selected_material=material,
        selected_genre=genre,
        selected_decade=decade,
        search=search,
    )


@app.route("/surprise")
def surprise():
    """Whisk the visitor away to a random look in the archive."""
    look_id = db.get_random_look_id()
    if look_id is None:
        return redirect(url_for("index"))
    return redirect(url_for("look_detail", look_id=look_id))


@app.route("/look/<int:look_id>")
def look_detail(look_id):
    look = db.get_look(look_id)
    if look is None:
        return "Look not found", 404
    other_looks = db.get_other_looks_for_character(look["character_id"], look_id)
    return render_template("look_detail.html", look=look, other_looks=other_looks)


@app.route("/mood/<color>")
def mood_board(color):
    """Every look tagged with a given color, across all films — the 'mood board' feature."""
    all_looks = db.get_all_looks()
    looks = [l for l in all_looks if color in l["colors"]]
    return render_template("mood_board.html", looks=looks, color=color, colors=db.COLOR_CATEGORIES)


@app.route("/add", methods=["GET", "POST"])
def add_look():
    if request.method == "POST":
        conn = db.get_connection()

        film_id = db.find_or_create_film(
            conn,
            request.form["film_title"].strip(),
            int(request.form["film_year"]),
            request.form.get("director", "").strip(),
            request.form.get("genre", "").strip(),
        )
        character_id = db.find_or_create_character(
            conn, request.form["character_name"].strip(), film_id
        )
        look_id = db.insert_look(
            conn,
            character_id,
            request.form.get("scene_label", "").strip(),
            request.form.get("designer", "").strip(),
            request.form.get("era_decade", "").strip(),
            request.form.get("description", "").strip(),
            request.form.get("image_url", "").strip(),
            request.form.getlist("colors"),
            request.form.getlist("materials"),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("look_detail", look_id=look_id))

    return render_template("add_look.html", colors=db.COLOR_CATEGORIES, materials=db.MATERIAL_CATEGORIES)


def ensure_seeded():
    """On first run against a fresh database, seed it with the starter dataset."""
    db.init_db()
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM films")
    film_count = cur.fetchone()["c"]
    conn.close()
    if film_count == 0:
        import seed
        seed.run()


if __name__ == "__main__":
    ensure_seeded()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
else:
    # Also ensure the schema exists + seed data when run under gunicorn (Render, etc.)
    ensure_seeded()
