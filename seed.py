"""
Populates the database with the starter dataset.
Run with: python seed.py
Safe to re-run — it truncates existing tables first.
"""
import db

DATA = [
    # (film_title, year, director, genre, character, [ (scene_label, designer, era_decade, description, colors, image_file), ... ])
    ("Marie Antoinette", 2006, "Sofia Coppola", "period-drama", "Marie Antoinette", [
        ("Cake & champagne scene", "Milena Canonero", "1770s",
         "A pastel confection of a gown, styled to look almost edible — part of the film's deliberately anachronistic, sugar-pop take on Versailles.",
         ["pastel-pink", "mint", "gold"], ""),
    ]),
    ("Pride & Prejudice", 2005, "Joe Wright", "period-drama", "Elizabeth Bennet", [
        ("Muddy-hem morning walk", "Jacqueline Durran", "1790s",
         "A simple cream empire-waist dress, deliberately less polished than her sisters' — costume as characterization.",
         ["ivory", "blue"], "elizabeth-bennet-prideandprejudice-hayfield.jpg"),
        ("Sick day at Netherfield", "Jacqueline Durran", "1790s",
         "A plain wool day dress worn while nursing a cold at Netherfield — deliberately unglamorous, in keeping with the film's grounded, lived-in take on Regency dress.",
         ["burgundy"], "keira-prideandprejudice-brownmonotone.jpg"),
    ]),
    ("Phantom Thread", 2017, "Paul Thomas Anderson", "period-drama", "The Countess", [
        ("Gala entrance", "Mark Bridges", "1950s",
         "A deep burgundy evening gown from the House of Woodcock, tailored with the obsessive precision the film is built around.",
         ["burgundy", "ivory"], ""),
    ]),
    ("Star Wars: Episode II", 2002, "George Lucas", "sci-fi", "Padmé Amidala", [
        ("Meadow picnic dress", "Trisha Biggar", "n/a",
         "A flowing, softly draped gown that reads almost medieval — a rare moment of romantic vulnerability in Padmé's wardrobe.",
         ["white", "gold"], "padme-ombredress.jpg"),
        ("Naboo diplomatic gown", "Trisha Biggar", "n/a",
         "An elaborate gold-and-cream gown with an ornate headpiece, part of Padmé's formal diplomatic wardrobe on Naboo.",
         ["gold", "ivory"], "padme-orange.jpg"),
    ]),
    ("Mad Max: Fury Road", 2015, "George Miller", "sci-fi", "Furiosa", [
        ("Wasteland warlord look", "Jenny Beavan", "n/a",
         "Rust-toned utility wear built from scavenged materials — practical, armored, and completely without vanity.",
         ["rust", "khaki"], ""),
    ]),
    ("The Devil Wears Prada", 2006, "David Frankel", "fashion-world", "Miranda Priestly", [
        ("Office entrance", "Patricia Field", "2000s",
         "A silver-grey power coat that announces her before she says a word.",
         ["silver", "navy"], ""),
        ("Boardroom pinstripe suit", "Patricia Field", "2000s",
         "A cropped pinstripe jacket and skirt worn over a stark white blouse — Miranda's daytime uniform of understated, terrifying authority.",
         ["black", "grey"], "miranda-devilwearsprada-blacksuit.jpg"),
        ("Fox fur exit coat", "Patricia Field", "2000s",
         "An oversized red fox fur coat, worn leaving the office — equal parts armor and spectacle.",
         ["burgundy", "black"], "miranda-devilwearsprada-redfur.jpg"),
    ]),
    ("The Devil Wears Prada", 2006, "David Frankel", "fashion-world", "Andy Sachs", [
        ("Paris finale look", "Patricia Field", "2000s",
         "The navy-and-cerulean transformation look, marking Andy's full arrival into the fashion world she once mocked.",
         ["navy", "blue"], ""),
        ("First day at Runway", "Patricia Field", "2000s",
         "The cable-knit sweater and plaid skirt Andy wears before her transformation — sensible, collegiate, completely wrong for the building she's walking into.",
         ["blue", "grey"], "andy-devilwearsprada-blyesweater.jpg"),
        ("Times Square trench", "Patricia Field", "2000s",
         "A cream trench thrown over a plaid skirt, marking the midpoint of Andy's wardrobe evolution.",
         ["ivory", "blue"], "andy-devilwearsprada-bluedress.jpg"),
        ("After-hours edge", "Patricia Field", "2000s",
         "A cropped leather jacket, skinny jeans, and knee-high boots — Andy fully fluent in the fashion world's off-duty uniform.",
         ["black", "rust"], "andy-devilwearsprada-leather.jpg"),
        ("Office hallway shift dress", "Patricia Field", "2000s",
         "A black shift dress with a crisp white collar and a strand of pearls, styled by Nigel for Andy's first real day looking the part.",
         ["black", "ivory"], "annehathaway-devilwearsprada-blackmini.jpg"),
    ]),
    ("The Devil Wears Prada", 2006, "David Frankel", "fashion-world", "Emily Charlton", [
        ("Senior assistant, on the phone", "Patricia Field", "2000s",
         "A structured black top with an asymmetric ruffled collar and a chain-and-stud belt — Emily's armor for surviving the Elias-Clark hallways.",
         ["black", "grey"], "emilyblunt-devilwearsprada-black.jpg"),
    ]),
    ("Breakfast at Tiffany's", 1961, "Blake Edwards", "fashion-world", "Holly Golightly", [
        ("Fifth Avenue window-shopping", "Hubert de Givenchy", "1960s",
         "The little black dress and pearls that became one of the most referenced silhouettes in film costume history.",
         ["black", "silver"], ""),
    ]),
    ("Beetlejuice", 1988, "Tim Burton", "horror", "Lydia Deetz", [
        ("Wedding/sacrifice dress", "Aggie Guerard Rodgers", "1980s",
         "A red gothic wedding gown that fuses bridal tradition with horror-movie dread.",
         ["red", "black"], ""),
    ]),
    ("The Addams Family", 1991, "Barry Sonnenfeld", "horror", "Morticia Addams", [
        ("Family portrait look", "Ruth Myers", "n/a",
         "The severe black silhouette with tendril-like hem, elegant and unmistakably gothic.",
         ["black", "green"], "morticia-addamsfamily.jpg"),
    ]),
    ("Moulin Rouge!", 2001, "Baz Luhrmann", "fashion-world", "Satine", [
        ("Diamond stage number", "Catherine Martin", "1900s",
         "A showgirl look dripping in red and black, built for maximum stage drama.",
         ["red", "black"], ""),
    ]),
    ("Frankenstein", 2025, "Guillermo del Toro", "horror", "Elizabeth Lavenza", [
        ("Debut introduction gown", "Kate Hawley", "1850s",
         "A turquoise-and-gold gown paired with an iridescent beetle-inspired necklace, introducing Elizabeth's insect motif in her first scene.",
         ["turquoise", "green", "gold"], "elizabeth-frankenstein-tealruffles.jpg"),
        ("Sheer nightgown, staircase scene", "Kate Hawley", "1850s",
         "A translucent ivory nightgown worn in a candlelit descent down a staircase, a classic gothic-romance visual moment.",
         ["ivory", "gold"], "elizabeth-frankenstein-whitenightgown.jpg"),
        ("Final bride look", "Kate Hawley", "1850s",
         "A bone-white gown with bandage-like textures and an exposed-ribcage motif, deliberately echoing the Creature's design.",
         ["white", "silver"], "elizabeth-frankenstein-bridal.jpg"),
        ("Bistro / day dress", "Kate Hawley", "1850s",
         "Custom-woven malachite-green silk with marbled velvet detailing, giving Elizabeth a luminous, almost otherworldly quality.",
         ["green", "gold"], "elizabeth-frankenstein-forestgreen.jpg"),
    ]),
    ("Portrait of a Lady on Fire", 2019, "Céline Sciamma", "period-drama", "Marianne", [
        ("Coastal walk, red dress", "Dorothée Guiraud", "1770s",
         "A single, stripped-down red dress that anchors Marianne's look throughout the film, following the director's one-outfit-per-character concept.",
         ["red"], ""),
    ]),
    ("The Favourite", 2018, "Yorgos Lanthimos", "period-drama", "Sarah Churchill", [
        ("Palace hunting look", "Sandy Powell", "1700s",
         "A severe black-and-white silhouette that blends period tailoring with a modern, almost punk sensibility.",
         ["black", "white"], ""),
    ]),
    ("Little Women", 2019, "Greta Gerwig", "period-drama", "Jo March", [
        ("Writing-desk attic scene", "Jacqueline Durran", "1860s",
         "A practical rust-toned dress reflecting Jo's independence and disinterest in the fashionable expectations placed on her sisters.",
         ["rust", "khaki"], ""),
    ]),
    ("Little Women", 2019, "Greta Gerwig", "period-drama", "Amy March", [
        ("Attic sketching, blue cape", "Jacqueline Durran", "1860s",
         "A powder-blue wool cape over a matching dress — Amy's quieter, more refined counterpoint to Jo's rust-toned practicality.",
         ["blue"], "florencepugh-littlewomen-bluecvape.jpg"),
    ]),
    ("Dune", 2021, "Denis Villeneuve", "sci-fi", "Chani", [
        ("Fremen stillsuit", "Jacqueline West", "n/a",
         "A functional desert stillsuit built from sand-toned gauze layered to evoke the rock and dust of Arrakis, designed with co-costume designer Bob Morgan.",
         ["khaki", "rust"], ""),
    ]),
    ("The Lord of the Rings: The Fellowship of the Ring", 2001, "Peter Jackson", "sci-fi", "Galadriel", [
        ("Mirror of Galadriel scene", "Ngila Dickson", "n/a",
         "A flowing white-and-gold gown that gives the Elven queen an otherworldly, almost luminous presence.",
         ["white", "gold", "silver"], ""),
    ]),
    ("Cruella", 2021, "Craig Gillespie", "fashion-world", "Cruella de Vil", [
        ("Runway crash entrance", "Jenny Beavan", "1970s",
         "A dramatic black-and-white couture gown built for a grand entrance, fusing punk attitude with high fashion.",
         ["black", "white", "red"], "emmastone-cruella-redblack.jpg"),
        ("Fireside red gown", "Jenny Beavan", "1970s",
         "A structured crimson gown with a dramatic train, worn for a quieter, more calculating moment by the fire.",
         ["red"], "emmastone-cruella-red.jpg"),
    ]),
    ("House of Gucci", 2021, "Ridley Scott", "fashion-world", "Patrizia Reggiani", [
        ("Low-cut red evening dress", "Janty Yates", "1970s",
         "A daringly cut red dress altered on set for more leg, part of Patrizia's rise into the world of Italian luxury fashion.",
         ["red"], ""),
    ]),
    ("Crimson Peak", 2015, "Guillermo del Toro", "horror", "Edith Cushing", [
        ("Allerdale Hall arrival", "Kate Hawley", "1900s",
         "A golden gothic gown that stands out against the decaying, snow-covered mansion, another del Toro/Hawley collaboration.",
         ["gold", "black"], ""),
    ]),
    ("Suspiria", 2018, "Luca Guadagnino", "horror", "Susie Bannion", [
        ("Dance academy rehearsal leotard", "Giulia Piersanti", "1970s",
         "A rich maroon leotard worn during dance classes, one of the few saturated color notes in the film's otherwise muted, foreboding palette.",
         ["burgundy", "rust"], ""),
    ]),
    ("Mr. & Mrs. Smith", 2005, "Doug Liman", "action", "Jane Smith", [
        ("Cocktail black dress, poster look", "", "2000s",
         "A fitted black cocktail dress slit to the thigh, holstered weapon included — the film's iconic double-exposure poster image.",
         ["black"], "angelina-mrandmrssmith-cover-blackdress.jpg"),
        ("Post-explosion white shirt", "", "2000s",
         "An oversized white shirt and red rain boots, worn walking away from a house leveled in a shootout — glamour as deadpan punchline.",
         ["white", "red"], "angelina-mrandmrssmith-oversizedwhiteshirt.jpg"),
    ]),
    ("Ocean's 8", 2018, "Gary Ross", "heist", "Daphne Kluger", [
        ("Met Gala centerpiece gown", "Sarah Edwards", "2010s",
         "A fuchsia off-shoulder gown paired with a diamond necklace worth the entire heist — Daphne playing the mark and the spectacle at once.",
         ["pink"], "annehathaway-oceans8-pinkgown.jpg"),
    ]),
    ("Ocean's 8", 2018, "Gary Ross", "heist", "Nine Ball", [
        ("Met Gala staircase entrance", "Sarah Edwards", "2010s",
         "A structured red mermaid gown worn descending the Met steps mid-heist — cool nerve dressed as red-carpet glamour.",
         ["red"], "rihanna-oceans8-redgown.jpg"),
    ]),
    ("Ocean's 8", 2018, "Gary Ross", "heist", "Debbie Ocean", [
        ("One-shoulder gold-beaded gown", "Sarah Edwards", "2010s",
         "A sheer, gold-embroidered gown worn as the crew's mastermind finally gets her night at the Gala she planned all along.",
         ["gold", "black"], "sandrabullock-oceans8-crystal.jpg"),
    ]),
    ("The Princess Diaries", 2001, "Garry Marshall", "coming-of-age", "Mia Thermopolis", [
        ("Coronation ball gown", "", "2000s",
         "An ivory gown embroidered with gold florals, worn with a tiara for Mia's formal introduction as Princess of Genovia.",
         ["ivory", "gold"], "annehathaway-princessdiaries-ballgown.jpg"),
    ]),
    ("Barbie", 2023, "Greta Gerwig", "comedy", "Barbie", [
        ("Beach day sailor set", "Jacqueline Durran", "n/a",
         "A striped halter top and shorts with a nautical wheel belt buckle — Barbie's default, endlessly cheerful beach uniform.",
         ["blue", "white"], "barbie-bluewhite-sailor.jpg"),
        ("Pink cowgirl western wear", "Jacqueline Durran", "n/a",
         "A magenta denim vest-and-pants set with a paisley bandana, worn riding into the real world.",
         ["pink"], "barbie-pinkdenim.jpg"),
        ("Gingham pool dress", "Jacqueline Durran", "n/a",
         "The pink-and-white gingham sundress that became the film's signature silhouette, worn by the pool in Barbieland.",
         ["pastel-pink", "white"], "barbie-pinkgingham.jpg"),
        ("Disco sequin jumpsuit", "Jacqueline Durran", "n/a",
         "An iridescent sequined jumpsuit, dance-floor ready, catching every color in the room.",
         ["silver", "pink"], "barbie-sparkle-jumpsuit.jpg"),
        ("Striped swim romper", "Jacqueline Durran", "n/a",
         "A black-and-white striped one-piece — a direct nod to the original 1959 Barbie doll's debut swimsuit.",
         ["black", "white"], "barbie-striped-romper.jpg"),
        ("Yellow tweed press suit", "Jacqueline Durran", "n/a",
         "A pastel tweed skirt suit with a bell-sleeve blouse and gold chain belt, worn on Barbie's press tour through the real world.",
         ["gold", "pastel-pink"], "barbie-yellowplaid.jpg"),
    ]),
    ("Clueless", 1995, "Amy Heckerling", "comedy", "Cher Horowitz", [
        ("Yellow plaid schoolgirl suit", "Mona May", "1990s",
         "The matching yellow plaid blazer and pleated skirt that defined '90s teen style — Beverly Hills prep as its own uniform.",
         ["gold"], "cher-clueless-plaidyellowsuit.jpg"),
    ]),
    ("Enchanted", 2007, "Kevin Lima", "fantasy", "Giselle", [
        ("Curtain-fabric gown", "", "2000s",
         "A gown Giselle stitches from a New York apartment's curtains, embroidered by hand with woodland creatures — animated fairy-tale habits colliding with the real world.",
         ["turquoise", "pink"], "giselle-enchanted-curtaindress.jpg"),
        ("Runaway wedding gown", "", "2000s",
         "A voluminous ivory ball gown with puffed sleeves, worn to a wedding Giselle ultimately walks away from.",
         ["ivory"], "giselle-enchanted-weddinggown.jpg"),
    ]),
    ("Legally Blonde", 2001, "Robert Luketic", "comedy", "Elle Woods", [
        ("Courtroom pink power suit", "", "2000s",
         "A coral-pink wrap dress worn to cross-examine a witness and win a murder trial — pink as a legal strategy.",
         ["pink"], "elle-legallyblonde-pink-courtroomsuit.jpg"),
    ]),
    ("Me Before You", 2016, "Thea Sharrock", "romance", "Louisa Clark", [
        ("Bumblebee tights", "", "2010s",
         "Striped bumblebee tights under a pleated navy skirt — Louisa's determinedly bright, slightly eccentric personal uniform.",
         ["navy", "gold"], "emilia-mebeforeyou-bumblebeetights.jpg"),
        ("Red dress, staircase", "", "2010s",
         "A simple red fit-and-flare dress worn for one of the film's pivotal quiet moments.",
         ["red"], "emiliaclarke-mebeforeyou-redgown.jpg"),
    ]),
    ("Mean Girls", 2004, "Mark Waters", "comedy", "Regina George", [
        ("Off-shoulder black sweater", "", "2000s",
         "An off-the-shoulder black sweater over low-rise jeans — Plastics-approved casual wear.",
         ["black"], "regina-meangirls-black-offshoulder.jpg"),
        ("Mall floral halter", "", "2000s",
         "A bright floral halter top worn on a mall trip — peak mid-2000s junior fashion.",
         ["pink"], "regina-meangirls-floraltank.jpg"),
    ]),
    ("Enola Holmes", 2020, "Harry Bradbeer", "period-drama", "Enola Holmes", [
        ("Crimson traveling gown", "Consolata Boyle", "1880s",
         "A deep red bustled traveling dress worn while investigating alone in London — practical enough to run in, striking enough to be remembered.",
         ["burgundy"], "enolaholmes-crimsongown.jpg"),
    ]),
    ("Wicked", 2024, "Jon M. Chu", "musical", "Glinda", [
        ("Behind-the-scenes ruffled robe", "Paul Tazewell", "n/a",
         "A rose-pink tulle robe with sculptural sleeve ruffles, worn between scenes at Shiz.",
         ["pink"], "glinda-wicked-pinknet.jpg"),
        ("‘Popular’ entrance gown", "Paul Tazewell", "n/a",
         "The iridescent pink ballgown and tiara for Glinda's signature bubble entrance.",
         ["pastel-pink"], "glinda-wicked-pinkruffles.jpg"),
        ("Travel skirt suit", "Paul Tazewell", "n/a",
         "A striped pink skirt suit with a small feathered hat, worn arriving at Shiz University.",
         ["pastel-pink", "silver"], "glinda-wicked-skirtsuit.jpg"),
    ]),
    ("13 Going on 30", 2004, "Gary Winick", "comedy", "Jenna Rink", [
        ("Razzle Dazzle mosaic dress", "", "2000s",
         "A color-blocked silk dress worn to lead an entire office party through a spontaneous 'Thriller' dance number.",
         ["green", "purple", "turquoise"], "jennifer-13goingon30-mosaicdress.jpg"),
        ("White biker jacket", "", "2000s",
         "A cream leather jacket worn window-shopping through New York, freshly transported into her 30-year-old life.",
         ["ivory", "khaki"], "jennifer-13goingon30-whitebikerjacket.jpg"),
    ]),
    ("Pretty Woman", 1990, "Garry Marshall", "romance", "Vivian Ward", [
        ("Brown polka-dot day dress", "Marilyn Vance", "1990s",
         "A brown-and-white polka dot dress worn to the polo match — Vivian's first fully successful pass at old-money dressing.",
         ["khaki"], "juliaroberts-prettywoman-brownpolka.jpg"),
    ]),
    ("How to Lose a Guy in 10 Days", 2003, "Donald Petrie", "romance", "Andie Anderson", [
        ("Butter-yellow satin gown", "", "2000s",
         "A bias-cut yellow satin gown worn to a black-tie diamond event — full old-Hollywood glamour.",
         ["gold"], "katehudson-howtoloseaguy-butteryellowgown.jpg"),
    ]),
    ("Atonement", 2007, "Joe Wright", "period-drama", "Cecilia Tallis", [
        ("Emerald green backless gown", "Jacqueline Durran", "1930s",
         "The bias-cut emerald silk gown from the library scene — one of the most referenced dresses in modern costume design.",
         ["green"], "keira-atonement-greendress.jpg"),
        ("Floral tea gown", "Jacqueline Durran", "1930s",
         "A sheer floral blouse and striped skirt worn in the garden before the family dinner that changes everything.",
         ["khaki", "pink"], "keira-atonement-floral.jpg"),
        ("Fountain slip", "Jacqueline Durran", "1930s",
         "A pale silk slip, soaked through after Cecilia dives into the fountain to retrieve a broken piece of a vase — one of the film's defining images.",
         ["ivory"], "keira-atonement-fountainslip.jpg"),
    ]),
    ("Cinderella", 2015, "Kenneth Branagh", "fantasy", "Cinderella", [
        ("Ball gown, grand staircase", "Sandy Powell", "n/a",
         "A cornflower-blue silk-organza gown, famously built from thousands of crystals and yards of tulle, worn descending the palace stairs.",
         ["blue"], "lilyjames-cinderella-gown.jpg"),
    ]),
    ("La La Land", 2016, "Damien Chazelle", "musical", "Mia Dolan", [
        ("Purple dress, dance rehearsal", "Mary Zophres", "2010s",
         "A deep plum halter dress worn twirling against a painted hillside backdrop during 'A Lovely Night.'",
         ["purple"], "mia-lalaland-purple.jpg"),
        ("Cobalt party dress", "Mary Zophres", "2010s",
         "A cobalt-blue chiffon dress worn to a Hollywood Hills party, one of the film's brightest, most saturated color notes.",
         ["blue"], "mia-lalaland-royalblue.jpg"),
        ("Yellow dress, city overlook", "Mary Zophres", "2010s",
         "The canary-yellow dress from the film's most-referenced promotional image, worn overlooking the city at dusk.",
         ["gold"], "mia-lalaland-yellowdress.jpg"),
    ]),
    ("The Notebook", 2004, "Nick Cassavetes", "romance", "Allie Hamilton", [
        ("Rowboat blue dress", "", "1940s",
         "A simple sky-blue day dress worn on a rowboat date among the swans — one of the film's quieter, most iconic images.",
         ["blue"], "rachel-notebook-babyblue.jpg"),
        ("Burgundy garden party dress", "", "1940s",
         "A burgundy dress with a matching flower-trimmed hat, worn to a formal garden engagement party.",
         ["burgundy"], "rachel-notebook-burgundy.jpg"),
        ("Bandana-print sundress", "", "1940s",
         "A crimson bandana-print sundress worn on a casual day out, eating ice cream by the water.",
         ["red"], "rachel-notebook-crimsondots.jpg"),
    ]),
    ("The Other Boleyn Girl", 2008, "Justin Chadwick", "period-drama", "Anne Boleyn", [
        ("Sage and gold damask gown", "", "1520s",
         "A sage-green and gold brocade gown with a jeweled French hood, worn at court as Anne begins to catch the King's eye.",
         ["green", "gold"], "natalie-anneboleyn-sagegown.jpg"),
    ]),
    ("Titanic", 1997, "James Cameron", "period-drama", "Rose DeWitt Bukater", [
        ("First-class dinner gown", "Deborah Lynn Scott", "1910s",
         "A beaded burgundy chiffon gown worn to Rose's first dinner aboard the Titanic, laced into a corset and a life she's already outgrown.",
         ["burgundy", "black"], "rose-titanic-diningown.jpg"),
    ]),
    ("Ready or Not", 2019, "Matt Bettinelli-Olpin & Tyler Gillett", "horror", "Grace", [
        ("Wedding dress, shotgun in hand", "", "2010s",
         "A lace wedding gown paired with a bandolier and a hunting shotgun — bridal tradition and survival horror colliding by midnight.",
         ["ivory"], "samaraweaving-readyornot-bridal.jpg"),
    ]),
]


def run():
    db.init_db()

    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE looks, characters, films RESTART IDENTITY CASCADE")
    conn.commit()

    for film_title, year, director, genre, char_name, looks in DATA:
        film_id = db.find_or_create_film(conn, film_title, year, director, genre)
        character_id = db.find_or_create_character(conn, char_name, film_id)
        for scene_label, designer, era, desc, colors, image_file in looks:
            image_url = f"/static/img/{image_file}" if image_file else ""
            db.insert_look(conn, character_id, scene_label, designer, era, desc, image_url, colors)
    conn.commit()

    cur.execute("SELECT COUNT(*) AS c FROM films")
    film_count = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM characters")
    char_count = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) AS c FROM looks")
    look_count = cur.fetchone()["c"]
    conn.close()

    print(f"Seeded {film_count} films, {char_count} characters, {look_count} looks.")


if __name__ == "__main__":
    run()
