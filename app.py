from flask import Flask, render_template, request, redirect, url_for
import os
import db

app = Flask(__name__)
app.jinja_env.globals["color_hex"] = lambda tag: db.COLOR_HEX.get(tag, "#999999")


@app.route("/")
def index():
    """Browse page — supports filtering by color, genre, and decade via query params."""
    color = request.args.get("color", "")
    genre = request.args.get("genre", "")
    decade = request.args.get("decade", "")

    looks = db.get_all_looks(genre=genre or None, decade=decade or None)

    if color:
        looks = [l for l in looks if color in l["colors"]]

    return render_template(
        "index.html",
        looks=looks,
        colors=db.COLOR_CATEGORIES,
        genres=db.get_distinct_genres(),
        decades=db.get_distinct_decades(),
        selected_color=color,
        selected_genre=genre,
        selected_decade=decade,
    )


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
        )
        conn.commit()
        conn.close()

        return redirect(url_for("look_detail", look_id=look_id))

    return render_template("add_look.html", colors=db.COLOR_CATEGORIES)


def ensure_seeded():
    """On platforms with ephemeral disks (like Render's free tier), the sqlite
    file won't persist between deploys — so seed automatically if empty."""
    db.init_db()
    conn = db.get_connection()
    film_count = conn.execute("SELECT COUNT(*) FROM films").fetchone()[0]
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
