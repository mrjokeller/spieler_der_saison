import sqlite3
import json
import os

DB_PATH = "/../data/"
JSON_PATH = "/../docs/data/"


# this function creates the filepath for files in the data folder
def data_path(file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_type = JSON_PATH if file.split(".")[1] == "json" else DB_PATH
    return script_dir + file_type + file


query_total_ranking = """
    WITH player_minutes AS (
        -- sum total minutes per player (regardless of player_points)
        SELECT
            player_id,
            SUM(minutes) AS total_minutes
        FROM
            player_data
        GROUP BY
            player_id
    )
    SELECT
        p.player_id AS player_id,
        p.name AS player_name,
        MAX(p.shirt_number) AS shirt_number,
        SUM(pp.points) AS total_points,
        COUNT(DISTINCT pp.game_id) AS games_played,
        pm.total_minutes,  -- minutes from aggregated table
        CASE
            WHEN pm.total_minutes >= 90
            THEN ROUND((SUM(pp.points) * 90.0 / NULLIF(pm.total_minutes, 0)), 2)
            ELSE NULL
        END AS points_per_90_minutes
    FROM
        player_points pp
    JOIN
        player p ON pp.player_id = p.player_id
    LEFT JOIN
        player_minutes pm ON pp.player_id = pm.player_id
    GROUP BY
        p.player_id, p.name
    ORDER BY
        total_points DESC;
"""

query_community_ranking = """
    WITH player_minutes AS (
        -- sum total minutes per player (regardless of player_points)
        SELECT
            player_id,
            SUM(minutes) AS total_minutes
        FROM
            player_data
        GROUP BY
            player_id
    )
    SELECT
        p.player_id AS player_id,
        p.name AS player_name,
        MAX(p.shirt_number) AS shirt_number,
        SUM(pp.points) AS total_points,
        COUNT(DISTINCT pp.game_id) AS games_played,
        pm.total_minutes,  -- minutes from aggregated table
        CASE
            WHEN pm.total_minutes >= 90
            THEN ROUND((SUM(pp.points) * 90.0 / NULLIF(pm.total_minutes, 0)), 2)
            ELSE NULL
        END AS points_per_90_minutes
    FROM
        player_points pp
    JOIN
        player p ON pp.player_id = p.player_id
    LEFT JOIN
        player_minutes pm ON pp.player_id = pm.player_id
    WHERE
        pp.source = "Community"
    GROUP BY
        p.player_id, p.name
    ORDER BY
        total_points DESC;
"""

query_riky_ranking = """
    WITH player_minutes AS (
        -- sum total minutes per player (regardless of player_points)
        SELECT
            player_id,
            SUM(minutes) AS total_minutes
        FROM
            player_data
        GROUP BY
            player_id
    )
    SELECT
        p.player_id AS player_id,
        p.name AS player_name,
        MAX(p.shirt_number) AS shirt_number,
        SUM(pp.points) AS total_points,
        COUNT(DISTINCT pp.game_id) AS games_played,
        pm.total_minutes,  -- minutes from aggregated table
        CASE
            WHEN pm.total_minutes >= 90
            THEN ROUND((SUM(pp.points) * 90.0 / NULLIF(pm.total_minutes, 0)), 2)
            ELSE NULL
        END AS points_per_90_minutes
    FROM
        player_points pp
    JOIN
        player p ON pp.player_id = p.player_id
    LEFT JOIN
        player_minutes pm ON pp.player_id = pm.player_id
    WHERE
        pp.source = "Riky Palm"
    GROUP BY
        p.player_id, p.name
    ORDER BY
        total_points DESC;
"""

query_sebastian_ranking = """
    WITH player_minutes AS (
        -- sum total minutes per player (regardless of player_points)
        SELECT
            player_id,
            SUM(minutes) AS total_minutes
        FROM
            player_data
        GROUP BY
            player_id
    )
    SELECT
        p.player_id AS player_id,
        p.name AS player_name,
        MAX(p.shirt_number) AS shirt_number,
        SUM(pp.points) AS total_points,
        COUNT(DISTINCT pp.game_id) AS games_played,
        pm.total_minutes,  -- minutes from aggregated table
        CASE
            WHEN pm.total_minutes >= 90
            THEN ROUND((SUM(pp.points) * 90.0 / NULLIF(pm.total_minutes, 0)), 2)
            ELSE NULL
        END AS points_per_90_minutes
    FROM
        player_points pp
    JOIN
        player p ON pp.player_id = p.player_id
    LEFT JOIN
        player_minutes pm ON pp.player_id = pm.player_id
    WHERE
        pp.source = "Sebastian Rose"
    GROUP BY
        p.player_id, p.name
    ORDER BY
        total_points DESC;
"""

query_line_chart = """
    WITH game_order AS (
        -- Spiele in der richtigen Reihenfolge (nach Datum)
        SELECT
            game_id,
            ROW_NUMBER() OVER (ORDER BY date) AS game_sequence
        FROM games
    ),
    player_points_with_sequence AS (
        -- Punkte pro Spieler und Spiel, mit Spiel-Reihenfolge
        SELECT
            p.player_id,
            p.name AS player_name,
            go.game_sequence,
            COALESCE(SUM(pp.points), 0) AS points
        FROM
            game_order go
        CROSS JOIN
            player p
        LEFT JOIN
            player_points pp ON p.player_id = pp.player_id AND go.game_id = pp.game_id
        GROUP BY
            p.player_id, p.name, go.game_sequence, go.game_id
    ),
    cumulative_points AS (
        -- Laufende Summe der Punkte pro Spieler
        SELECT
            player_id,
            player_name,
            game_sequence,
            points,
            SUM(points) OVER (
                PARTITION BY player_id
                ORDER BY game_sequence
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_points
        FROM
            player_points_with_sequence
    ),
    total_points_per_player AS (
        -- Gesamtpunkte pro Spieler berechnen
        SELECT
            player_id,
            player_name,
            MAX(cumulative_points) AS total_points  -- Letzter Wert der kumulativen Summe = Gesamtpunkte
        FROM
            cumulative_points
        GROUP BY
            player_id, player_name
    )
    -- Top 10 Spieler nach Gesamtpunkten
    SELECT
        cp.player_name AS label,
        GROUP_CONCAT(cp.cumulative_points, ', ') AS data
    FROM
        cumulative_points cp
    JOIN
        total_points_per_player tp ON cp.player_id = tp.player_id
    WHERE
        tp.player_id IN (
            SELECT player_id
            FROM total_points_per_player
            ORDER BY total_points DESC
            LIMIT 10
        )
    GROUP BY
        cp.player_name
    ORDER BY
        tp.total_points DESC;

"""


def export_ranking_to_json(db_name, output_file, query):
    # set connection to sqlite database
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # make query
    c.execute(query)
    ranking = c.fetchall()

    # transform data into dictionaries
    ranking_list = []
    for row in ranking:
        ranking_list.append(dict(row))

    # save json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ranking_list, f, indent=4, ensure_ascii=False)

    conn.close()
    print(f"Ranking was exported succesfully to {output_file}.")


def export_to_chart(db_name, output_file, query):
    # set connection to sqlite database
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # make query
    c.execute(query)
    ranking = c.fetchall()

    chart_data = []
    for label, data_str in ranking:
        data = [int(point) for point in data_str.split(", ")]
        chart_data.append({"label": label, "data": data, "fill": False})

    # save json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chart_data, f, indent=4, ensure_ascii=False)

    conn.close()
    print(f"Ranking was exported succesfully to {output_file}.")


output_files = [
    "player_ranking.json",
    "player_ranking_community.json",
    "player_ranking_riky.json",
    "player_ranking_sebastian.json",
]
queries = [
    query_total_ranking,
    query_community_ranking,
    query_riky_ranking,
    query_sebastian_ranking,
]

for i in range(4):
    export_ranking_to_json(data_path("data.db"), data_path(output_files[i]), queries[i])

export_to_chart(
    db_name=data_path("data.db"),
    output_file=data_path("line_chart_data.json"),
    query=query_line_chart,
)
