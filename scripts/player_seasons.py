from config import DEFAULT_DB_NAME
import sqlite3

conn = sqlite3.connect(DEFAULT_DB_NAME)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def show_players():
    players = cur.execute("SELECT * FROM players ORDER BY name").fetchall()
    print("\n--- SPIELER ---")
    for p in players:
        print(f"[{p['player_id']}] {p['name']}")

def show_seasons():
    seasons = cur.execute("SELECT * FROM seasons ORDER BY label").fetchall()
    print("\n--- SAISONS ---")
    for s in seasons:
        print(f"[{s['season_id']}] {s['label']}")

def show_positions():
    positions = cur.execute("SELECT * FROM positions ORDER BY position_id").fetchall()
    print("\n--- POSITIONEN ---")
    for p in positions:
        print(f"[{p['position_id']}] {p['name']} ({p['short_name']})")

def show_existing(player_id):
    entries = cur.execute("""
        SELECT s.label, ps.shirt_number, p.name as position
        FROM player_seasons ps
        JOIN seasons s ON ps.season_id = s.season_id
        JOIN positions p ON ps.position_id = p.position_id
        WHERE ps.player_id = ?
        ORDER BY s.label
    """, (player_id,)).fetchall()
    if entries:
        print("\n  Bereits eingetragen:")
        for e in entries:
            print(f"  → {e['label']} | #{e['shirt_number']} | {e['position']}")

while True:
    show_players()
    player_input = input("\nSpieler ID (oder 'q' zum Beenden): ").strip()
    if player_input.lower() == 'q':
        break

    player_id = int(player_input)
    player = cur.execute("SELECT name FROM players WHERE player_id = ?", (player_id,)).fetchone()
    if not player:
        print("✗ Spieler nicht gefunden!")
        continue

    print(f"\nGewählt: {player['name']}")
    show_existing(player_id)

    show_positions()
    position_id = int(input("\nPosition ID: "))
    shirt_number = int(input("Trikotnummer: "))

    show_seasons()
    print("\nSaison IDs eingeben (kommagetrennt, z.B. 1,2,3):")
    season_input = input("Saison IDs: ").strip()
    season_ids = [int(s.strip()) for s in season_input.split(",")]

    # Kontrolle
    position = cur.execute("SELECT name FROM positions WHERE position_id = ?", (position_id,)).fetchone()
    print(f"\nEinträge für {player['name']} | #{shirt_number} | {position['name']}:")
    for sid in season_ids:
        season = cur.execute("SELECT label FROM seasons WHERE season_id = ?", (sid,)).fetchone()
        print(f"  → {season['label']}")

    confirm = input("\nAlle bestätigen? (j/n): ").strip().lower()
    if confirm == "j":
        success, skipped = 0, 0
        for sid in season_ids:
            try:
                cur.execute("""
                    INSERT INTO player_seasons (player_id, season_id, shirt_number, position_id)
                    VALUES (?, ?, ?, ?)
                """, (player_id, sid, shirt_number, position_id))
                success += 1
            except sqlite3.IntegrityError:
                skipped += 1
        conn.commit()
        print(f"✓ {success} Einträge gespeichert, {skipped} übersprungen (bereits vorhanden).")
    else:
        print("Abgebrochen.")

conn.close()
print("\nFertig!")
