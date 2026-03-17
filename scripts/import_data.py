import sqlite3
import json
import os

DB_PATH = '/../data/'
JSON_PATH = '/../docs/data/'


# this function creates the filepath for files in the data folder
def data_path(file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_type = JSON_PATH if file.split('.')[1] == 'json' else DB_PATH
    path = script_dir + file_type + file
    print(path)
    return path

query_total_ranking = """
    SELECT
        p.name AS player_name,
        p.shirt_number,
        SUM(pp.points) AS total_points
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
    db_name=data_path("data.db"),
    output_file=data_path("player_ranking.json"),
    query=query_total_ranking,
)
