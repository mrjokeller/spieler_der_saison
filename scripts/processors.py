from typing import List, Dict, Any


def build_progression_chart_data(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Formt die Rohdaten aus stats.points_progression in Chart.js-kompatibles
    Format um: ein Objekt pro Spieler mit label + data-Array.
    """
    players: dict[int, dict[str, Any]] = {}

    for row in rows:
        pid = row["player_id"]
        if pid not in players:
            players[pid] = {"label": row["player_name"], "data": []}
        players[pid]["data"].append(row["points"])

    return list(players.values())


def longest_streak(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Erwartet Rohdaten aus points_progression (pro Spieler, chronologisch,
    kumulierte Punkte pro Spiel-Sequenz) und berechnet die längste Serie
    aufeinanderfolgender Spiele mit Punktezuwachs.
    """
    players: dict[int, dict[str, Any]] = {}

    for row in rows:
        pid = row["player_id"]
        if pid not in players:
            players[pid] = {
                "player_id": pid,
                "player_name": row["player_name"],
                "_previous_points": 0,
                "_current_streak": 0,
                "longest_streak": 0,
            }

        player = players[pid]
        if row["points"] > player["_previous_points"]:
            player["_current_streak"] += 1
            player["longest_streak"] = max(
                player["longest_streak"], player["_current_streak"]
            )
        else:
            player["_current_streak"] = 0

        player["_previous_points"] = row["points"]

    result = [
        {
            "player_id": p["player_id"],
            "player_name": p["player_name"],
            "longest_streak": p["longest_streak"],
        }
        for p in players.values()
    ]
    return sorted(result, key=lambda x: x["longest_streak"], reverse=True)
