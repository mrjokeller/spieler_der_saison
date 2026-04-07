def query_ranking(source):
    """Returns the query for the player ranking for the given source."""
    return f"""
            SELECT * FROM player_ranking_view
            WHERE source = "{source}"
            ORDER BY total_points DESC;
        """


query_total_ranking = """
    WITH player_minutes AS (
        SELECT
            player_id,
            SUM(minutes) AS total_minutes,
            COUNT(DISTINCT game_id) AS games_played
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
        pm.games_played,
        pm.total_minutes,
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
