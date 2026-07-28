# backend/exporters/jobs.py
"""
Zentrale Liste aller Export-Jobs. Neue Auswertung = neuer Eintrag hier,
kein Code-Duplizieren in main.py mehr nötig.
"""

from base import ExportJob
from processors import longest_streak, build_progression_chart_data
import queries

EXPORT_JOBS: list[ExportJob] = [
    ExportJob(
        name="Gesamt-Ranking",
        query_func=queries.total_ranking,
        query_kwargs={"season_id": 2526},
        output_file="total_ranking.json",
    ),
    ExportJob(
        name="Community-Ranking",
        query_func=queries.ranking_by_source,
        query_kwargs={"source": "Community", "season_id": 2526},
        output_file="community_ranking.json",
    ),
    ExportJob(
        name="Riky-Ranking",
        query_func=queries.ranking_by_source,
        query_kwargs={"source": "Riky Palm", "season_id": 2526},
        output_file="riky_ranking.json",
    ),
    ExportJob(
        name="Sebastian-Ranking",
        query_func=queries.ranking_by_source,
        query_kwargs={"source": "Sebastian Rose", "season_id": 2526},
        output_file="sebastian_ranking.json",
    ),
    ExportJob(
        name="Heimspiele-Ranking",
        query_func=queries.ranking_by_side,
        query_kwargs={"side": "home", "season_id": 2526},
        output_file="home_ranking.json",
    ),
    ExportJob(
        name="Auswärtsspiele-Ranking",
        query_func=queries.ranking_by_side,
        query_kwargs={"side": "away", "season_id": 2526},
        output_file="away_ranking.json",
    ),
    ExportJob(
        name="Bundesliga-Ranking",
        query_func=queries.ranking_by_competition,
        query_kwargs={"competition_name": "Bundesliga", "season_id": 2526},
        output_file="bundesliga_ranking.json",
    ),
    ExportJob(
        name="Europa League-Ranking",
        query_func=queries.ranking_by_competition,
        query_kwargs={"competition_name": "Europa League", "season_id": 2526},
        output_file="euroleague_ranking.json",
    ),
    ExportJob(
        name="DFB-Pokal-Ranking",
        query_func=queries.ranking_by_competition,
        query_kwargs={"competition_name": "DFB-Pokal", "season_id": 2526},
        output_file="dfbpokal_ranking.json",
    ),
    ExportJob(
        name="Meiste Stimmen",
        query_func=queries.most_votes,
        query_kwargs={"season_id": 2526},
        output_file="votes_ranking.json",
    ),
    ExportJob(
        name="Höchste Punktzahl in einem Spiel",
        query_func=queries.highest_single_game_points,
        query_kwargs={"season_id": 2526},
        output_file="most_points_in_game_ranking.json",
    ),
    ExportJob(
        name="Längster Streak",
        query_func=queries.points_progression,
        query_kwargs={"season_id": 2526},
        processor=longest_streak,
        output_file="longest_streak_ranking.json",
    ),
    ExportJob(
        name="Punkteverlauf (Chart)",
        query_func=queries.points_progression,
        query_kwargs={"season_id": 2526},
        processor=build_progression_chart_data,
        output_file="points_progression_chart.json",
    ),
]
