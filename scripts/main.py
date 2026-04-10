from queries import (
    query_total_ranking,
    query_ranking,
    query_line_chart,
    query_most_points,
)
from db_utils import execute_query
from export_utils import export_to_json, process_and_export
from config import DEFAULT_DB_NAME, JSON_PATH, TEST_JSON_PATH
from processors import prepare_chart_data

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
        "query": query_line_chart,
        "output_file": "line_chart_data.json",
        "processor": prepare_chart_data,
        "active": False,
    },
    {
        "query": query_most_points,
        "output_file": "most_points_in_game.json",
        "processor": None,
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
