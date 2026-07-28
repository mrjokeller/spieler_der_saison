def total_ranking(season_id: int | None = None) -> tuple[str, tuple]:
    """
    Gesamt-Ranking aller Spieler,
    optional gefiltert nach Saison.
    """
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (season_id,) if season_id else ()

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            pos.name AS position_name,
            COUNT(DISTINCT pp.game_id) AS games_played,
            SUM(pd.minutes) AS total_minutes,
            SUM(pp.points) AS total_points,
            ROUND(SUM(pp.points) * 90.0 / NULLIF(SUM(pd.minutes), 0), 2) AS points_per_90
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        LEFT JOIN player_data pd
            ON pd.player_id = pp.player_id AND pd.game_id = pp.game_id
        LEFT JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        LEFT JOIN positions pos
            ON pos.position_id = ps.position_id
        WHERE 1=1 {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number, pos.name
        ORDER BY total_points DESC;
    """
    return query, params


def ranking_by_source(source: str, season_id: int | None = None) -> tuple[str, tuple]:
    """Ranking gefiltert nach Punktequelle ()'Community', 'Riky', 'Sebastian')."""
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (source, season_id) if season_id else (source,)

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            COUNT(DISTINCT pp.game_id) AS games_played,
            SUM(pd.minutes) AS total_minutes,
            SUM(pp.points) AS total_points,
            ROUND(SUM(pp.points) * 90.0 / NULLIF(SUM(pd.minutes), 0), 2) AS points_per_90
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        LEFT JOIN player_data pd
            ON pd.player_id = pp.player_id AND pd.game_id = pp.game_id
        LEFT JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        WHERE pp.source = ? {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number
        ORDER BY total_points DESC;
    """
    return query, params


def ranking_by_position(
    position_name: str, season_id: int | None = None
) -> tuple[str, tuple]:
    """Ranking gefiltert nach Position"""
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (position_name, season_id) if season_id else (position_name,)

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            SUM(pp.points) AS total_points
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        JOIN positions pos ON pos.position_id = ps.position_id
        WHERE pos.name = ? {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number
        ORDER BY total_points DESC;
    """
    return query, params


def ranking_by_side(side: str, season_id: int | None = None) -> tuple[str, tuple]:
    """Ranking gefiltert nach Heim/Auswärts."""
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (side, season_id) if season_id else (side,)

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            SUM(pp.points) AS total_points
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        LEFT JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        WHERE g.side = ? {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number
        ORDER BY total_points DESC;
    """
    return query, params


def ranking_by_competition(
    competition_name: str, season_id: int | None = None
) -> tuple[str, tuple]:
    """Ranking gefiltert nach Wettbewerb (Bundesliga, DFB-Pokal, ...)."""
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (competition_name, season_id) if season_id else (competition_name,)

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            SUM(pp.points) AS total_points
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        JOIN competitions c ON c.competition_id = g.competition_id
        LEFT JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        WHERE c.name = ? {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number
        ORDER BY total_points DESC;
    """
    return query, params

"""Spezial-Auswertungen: Stimmen, Höchstwerte, Streaks, Formkurve."""


def most_votes(season_id: int | None = None) -> tuple[str, tuple]:
    season_filter = "AND g.season_id = ?" if season_id else ""
    params = (season_id,) if season_id else ()

    query = f"""
        SELECT
            p.player_id,
            p.name AS player_name,
            ps.shirt_number,
            SUM(pp.votes) AS total_votes
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        LEFT JOIN player_seasons ps
            ON ps.player_id = p.player_id AND ps.season_id = g.season_id
        WHERE pp.source = 'Community' {season_filter}
        GROUP BY p.player_id, p.name, ps.shirt_number
        ORDER BY total_votes DESC;
    """
    return query, params


def highest_single_game_points(limit: int = 20) -> tuple[str, tuple]:
    """Höchste Einzelspiel-Punktzahl je Spieler+Spiel (aggregiert über Quellen)."""
    query = """
        SELECT
            p.player_id,
            p.name AS player_name,
            g.game_id,
            g.date,
            o.name AS opponent_name,
            SUM(pp.points) AS game_points
        FROM player_points pp
        JOIN players p ON p.player_id = pp.player_id
        JOIN games g ON g.game_id = pp.game_id
        JOIN opponents o ON o.opponent_id = g.opponent_id
        GROUP BY p.player_id, g.game_id
        ORDER BY game_points DESC
        LIMIT ?;
    """
    return query, (limit,)


def points_progression(source: str | None = None) -> tuple[str, tuple]:
    """
    Rohdaten für Streak-/Formkurven-Berechnung:
    Punkte pro Spieler in chronologischer Spielreihenfolge.
    Aggregation/Streak-Logik passiert im Processor, nicht in SQL.
    """
    source_filter = "AND pp.source = ?" if source else ""
    params = (source,) if source else ()

    query = f"""
        WITH game_order AS (
            SELECT game_id, ROW_NUMBER() OVER (ORDER BY date) AS game_sequence
            FROM games
        )
        SELECT
            p.player_id,
            p.name AS player_name,
            go.game_sequence,
            COALESCE(SUM(pp.points), 0) AS points
        FROM game_order go
        CROSS JOIN players p
        LEFT JOIN player_points pp
            ON pp.player_id = p.player_id AND pp.game_id = go.game_id {source_filter}
        GROUP BY p.player_id, p.name, go.game_sequence
        ORDER BY p.player_id, go.game_sequence;
    """
    return query, params


def all_seasons() -> tuple[str, tuple]:
    return "SELECT season_id, label, active FROM seasons ORDER BY start_date DESC;", ()


def all_competitions() -> tuple[str, tuple]:
    return (
        "SELECT competition_id, name, short_name FROM competitions ORDER BY name;",
        (),
    )


def all_positions() -> tuple[str, tuple]:
    return "SELECT position_id, name, short_name FROM positions;", ()
