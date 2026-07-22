"""
Populates costumed.db with the starter dataset.
Run with: python seed.py
Safe to re-run — it deletes the existing db file first.
"""
import os
import db

DATA = [
    # (film_title, year, director, genre, character, [ (scene_label, designer, era_decade, description, colors), ... ])
    ("Marie Antoinette", 2006, "Sofia Coppola", "period-drama", "Marie Antoinette", [
        ("Cake & champagne scene", "Milena Canonero", "1770s",
         "A pastel confection of a gown, styled to look almost edible — part of the film's deliberately anachronistic, sugar-pop take on Versailles.",
         ["pastel-pink", "mint", "gold"]),
    ]),
    ("Pride & Prejudice", 2005, "Joe Wright", "period-drama", "Elizabeth Bennet", [
        ("Muddy-hem morning walk", "Jacqueline Durran", "1790s",
         "A simple cream empire-waist dress, deliberately less polished than her sisters' — costume as characterization.",
         ["ivory", "blue"]),
    ]),
    ("Phantom Thread", 2017, "Paul Thomas Anderson", "period-drama", "The Countess", [
        ("Gala entrance", "Mark Bridges", "1950s",
         "A deep burgundy evening gown from the House of Woodcock, tailored with the obsessive precision the film is built around.",
         ["burgundy", "ivory"]),
    ]),
    ("Star Wars: Episode II", 2002, "George Lucas", "sci-fi", "Padmé Amidala", [
        ("Meadow picnic dress", "Trisha Biggar", "n/a",
         "A flowing, softly draped gown that reads almost medieval — a rare moment of romantic vulnerability in Padmé's wardrobe.",
         ["white", "gold"]),
    ]),
    ("Mad Max: Fury Road", 2015, "George Miller", "sci-fi", "Furiosa", [
        ("Wasteland warlord look", "Jenny Beavan", "n/a",
         "Rust-toned utility wear built from scavenged materials — practical, armored, and completely without vanity.",
         ["rust", "khaki"]),
    ]),
    ("The Devil Wears Prada", 2006, "David Frankel", "fashion-world", "Miranda Priestly", [
        ("Office entrance", "Patricia Field", "2000s",
         "A silver-grey power coat that announces her before she says a word.",
         ["silver", "navy"]),
    ]),
    ("The Devil Wears Prada", 2006, "David Frankel", "fashion-world", "Andy Sachs", [
        ("Paris finale look", "Patricia Field", "2000s",
         "The navy-and-cerulean transformation look, marking Andy's full arrival into the fashion world she once mocked.",
         ["navy", "blue"]),
    ]),
    ("Breakfast at Tiffany's", 1961, "Blake Edwards", "fashion-world", "Holly Golightly", [
        ("Fifth Avenue window-shopping", "Hubert de Givenchy", "1960s",
         "The little black dress and pearls that became one of the most referenced silhouettes in film costume history.",
         ["black", "silver"]),
    ]),
    ("Beetlejuice", 1988, "Tim Burton", "horror", "Lydia Deetz", [
        ("Wedding/sacrifice dress", "Aggie Guerard Rodgers", "1980s",
         "A red gothic wedding gown that fuses bridal tradition with horror-movie dread.",
         ["red", "black"]),
    ]),
    ("The Addams Family", 1991, "Barry Sonnenfeld", "horror", "Morticia Addams", [
        ("Family portrait look", "Ruth Myers", "n/a",
         "The severe black silhouette with tendril-like hem, elegant and unmistakably gothic.",
         ["black", "green"]),
    ]),
    ("Moulin Rouge!", 2001, "Baz Luhrmann", "fashion-world", "Satine", [
        ("Diamond stage number", "Catherine Martin", "1900s",
         "A showgirl look dripping in red and black, built for maximum stage drama.",
         ["red", "black"]),
    ]),
    ("Frankenstein", 2025, "Guillermo del Toro", "horror", "Elizabeth Lavenza", [
        ("Debut introduction gown", "Kate Hawley", "1850s",
         "A turquoise-and-gold gown paired with an iridescent beetle-inspired necklace, introducing Elizabeth's insect motif in her first scene.",
         ["turquoise", "green", "gold"]),
        ("Sheer nightgown, staircase scene", "Kate Hawley", "1850s",
         "A translucent ivory nightgown worn in a candlelit descent down a staircase, a classic gothic-romance visual moment.",
         ["ivory", "gold"]),
        ("Final bride look", "Kate Hawley", "1850s",
         "A bone-white gown with bandage-like textures and an exposed-ribcage motif, deliberately echoing the Creature's design.",
         ["white", "silver"]),
        ("Bistro / day dress", "Kate Hawley", "1850s",
         "Custom-woven malachite-green silk with marbled velvet detailing, giving Elizabeth a luminous, almost otherworldly quality.",
         ["green", "gold"]),
    ]),
    ("Portrait of a Lady on Fire", 2019, "Céline Sciamma", "period-drama", "Marianne", [
        ("Coastal walk, red dress", "Dorothée Guiraud", "1770s",
         "A single, stripped-down red dress that anchors Marianne's look throughout the film, following the director's one-outfit-per-character concept.",
         ["red"]),
    ]),
    ("The Favourite", 2018, "Yorgos Lanthimos", "period-drama", "Sarah Churchill", [
        ("Palace hunting look", "Sandy Powell", "1700s",
         "A severe black-and-white silhouette that blends period tailoring with a modern, almost punk sensibility.",
         ["black", "white"]),
    ]),
    ("Little Women", 2019, "Greta Gerwig", "period-drama", "Jo March", [
        ("Writing-desk attic scene", "Jacqueline Durran", "1860s",
         "A practical rust-toned dress reflecting Jo's independence and disinterest in the fashionable expectations placed on her sisters.",
         ["rust", "khaki"]),
    ]),
    ("Dune", 2021, "Denis Villeneuve", "sci-fi", "Chani", [
        ("Fremen stillsuit", "Jacqueline West", "n/a",
         "A functional desert stillsuit built from sand-toned gauze layered to evoke the rock and dust of Arrakis, designed with co-costume designer Bob Morgan.",
         ["khaki", "rust"]),
    ]),
    ("The Lord of the Rings: The Fellowship of the Ring", 2001, "Peter Jackson", "sci-fi", "Galadriel", [
        ("Mirror of Galadriel scene", "Ngila Dickson", "n/a",
         "A flowing white-and-gold gown that gives the Elven queen an otherworldly, almost luminous presence.",
         ["white", "gold", "silver"]),
    ]),
    ("Cruella", 2021, "Craig Gillespie", "fashion-world", "Cruella de Vil", [
        ("Runway crash entrance", "Jenny Beavan", "1970s",
         "A dramatic black-and-white couture gown built for a grand entrance, fusing punk attitude with high fashion.",
         ["black", "white", "red"]),
    ]),
    ("House of Gucci", 2021, "Ridley Scott", "fashion-world", "Patrizia Reggiani", [
        ("Low-cut red evening dress", "Janty Yates", "1970s",
         "A daringly cut red dress altered on set for more leg, part of Patrizia's rise into the world of Italian luxury fashion.",
         ["red"]),
    ]),
    ("Crimson Peak", 2015, "Guillermo del Toro", "horror", "Edith Cushing", [
        ("Allerdale Hall arrival", "Kate Hawley", "1900s",
         "A golden gothic gown that stands out against the decaying, snow-covered mansion, another del Toro/Hawley collaboration.",
         ["gold", "black"]),
    ]),
    ("Suspiria", 2018, "Luca Guadagnino", "horror", "Susie Bannion", [
        ("Dance academy rehearsal leotard", "Giulia Piersanti", "1970s",
         "A rich maroon leotard worn during dance classes, one of the few saturated color notes in the film's otherwise muted, foreboding palette.",
         ["burgundy", "rust"]),
    ]),
]


def run():
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()

    conn = db.get_connection()
    for film_title, year, director, genre, char_name, looks in DATA:
        film_id = db.find_or_create_film(conn, film_title, year, director, genre)
        character_id = db.find_or_create_character(conn, char_name, film_id)
        for scene_label, designer, era, desc, colors in looks:
            db.insert_look(conn, character_id, scene_label, designer, era, desc, "", colors)
    conn.commit()

    film_count = conn.execute("SELECT COUNT(*) FROM films").fetchone()[0]
    char_count = conn.execute("SELECT COUNT(*) FROM characters").fetchone()[0]
    look_count = conn.execute("SELECT COUNT(*) FROM looks").fetchone()[0]
    conn.close()

    print(f"Seeded {film_count} films, {char_count} characters, {look_count} looks.")


if __name__ == "__main__":
    run()
