import sqlite3
from config import DEFAULT_DB_NAME

conn = sqlite3.connect(DEFAULT_DB_NAME)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

DEFAULT_COUNTRY = "Deutschland"

opponents = cur.execute("SELECT * FROM opponents ORDER BY name").fetchall()

print(f"Insgesamt {len(opponents)} Gegner\n")

for opp in opponents:
    print(f"\n[{opp['opponent_id']}] {opp['name']}")
    print(f"  Short: {opp['short_name'] or '–'} | Land: {opp['country'] or DEFAULT_COUNTRY}")

    name_input = input(f"  Neuer Name (Enter = behalten): ").strip()
    short_input = input(f"  Neuer Short Name (Enter = behalten): ").strip()
    country_input = input(f"  Land (Enter = '{opp['country'] or DEFAULT_COUNTRY}'): ").strip()

    name = name_input if name_input else opp['name']
    short = short_input if short_input else opp['short_name']
    country = country_input if country_input else (opp['country'] or DEFAULT_COUNTRY)

    if name_input or short_input or country_input:
        cur.execute("""
            UPDATE opponents SET name = ?, short_name = ?, country = ? WHERE opponent_id = ?
        """, (name, short, country, opp['opponent_id']))
        conn.commit()
        print("  ✓ Gespeichert")
    else:
        print("  → Übersprungen")

conn.close()
print("\nFertig!")
