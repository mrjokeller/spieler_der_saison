import sqlite3
import json
import os
from dotenv import load_dotenv


# this function creates the filepath for files in the data folder
def data_path_for(file):
    load_dotenv()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path_env = os.getenv("DATA_PATH")
    data_path = os.path.join(script_dir, data_path_env)
    return data_path + file


query_total_ranking = """
    SELECT
        p.name AS player_name,
        p.shirt_number,
        SUM(pp.points) AS total_points,
        COUNT(pp.game_id) AS played_games,
        AVG(pp.points) AS avg_points
    FROM
        player_points pp
    JOIN
        player p ON pp.player_id = p.player_id
    GROUP BY
        pp.player_id
    ORDER BY
        total_points DESC;
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


export_ranking_to_json(
    db_name=data_path_for("data.db"),
    output_file=data_path_for("player_ranking.json"),
    query=query_total_ranking,
)
