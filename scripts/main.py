from queries import (
    query_total_ranking,
    query_ranking,
    query_position_ranking,
    query_side_ranking,
    query_competition_ranking,
    query_points_progression,
    query_most_points,
    query_most_votes
)
from db_utils import execute_query
from export_utils import export_to_json, process_and_export
from config import DEFAULT_DB_NAME, JSON_PATH, TEST_JSON_PATH
from processors import longest_streak

is_test = False
export_path = TEST_JSON_PATH if is_test else JSON_PATH

EXPORT_TASKS = [
    {
        "query": query_total_ranking,
        "output_file": "player_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_ranking("Community"),
        "output_file": "player_ranking_community.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_ranking("Riky Palm"),
        "output_file": "player_ranking_riky.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_ranking("Sebastian Rose"),
        "output_file": "player_ranking_sebastian.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_position_ranking("Angriff"),
        "output_file": "attack_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_position_ranking("Mittelfeld"),
        "output_file": "midfield_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_position_ranking("Defensive"),
        "output_file": "defense_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_side_ranking("home"),
        "output_file": "home_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_side_ranking("away"),
        "output_file": "away_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_competition_ranking("Bundesliga"),
        "output_file": "bundesliga_ranking.json",
        "processor": None,
        "active": True
    },
    {
        "query": query_competition_ranking("Europa League"),
        "output_file": "euroleague_ranking.json",
        "processor": None,
        "active": True
    },
    {
        "query": query_competition_ranking("DFB-Pokal"),
        "output_file": "dfbpokal_ranking.json",
        "processor": None,
        "active": True
    },
    {
        "query": query_most_votes,
        "output_file": "votes_ranking.json",
        "processor": None,
        "active": True
    },
    {
        "query": query_most_points,
        "output_file": "most_points_in_game_ranking.json",
        "processor": None,
        "active": True,
    },
    {
        "query": query_points_progression,
        "output_file": "longest_streak_ranking.json",
        "processor": longest_streak,
        "active": True,
    },
]


def run_exports():
    for task in EXPORT_TASKS:
        print(f"trying to run task for {task['output_file']}.")
        if task["active"] is False:
            print(f"skipping task for {task['output_file']}.")
            continue
        if task["processor"] is None:
            # default process
            data = execute_query(DEFAULT_DB_NAME, task["query"])
            export_to_json(data, export_path + task["output_file"])
        else:
            # export with processing
            process_and_export(
                db_path=DEFAULT_DB_NAME,
                query=task["query"],
                processor=task["processor"],
                output_path=export_path + task["output_file"],
            )


if __name__ == "__main__":
    run_exports()
