import sqlite3
import json
import os
from dotenv import load_dotenv


def export_ranking_to_json(db_name, output_file):
    # set connection to sqlite database
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # query the data
    query = '''
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
'''

    # make query
    c.execute(query)
    ranking = c.fetchall()

    # transform data into dictionaries
    ranking_list = []
    for row in ranking:
        ranking_list.append(dict(row))

    # save json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ranking_list, f, indent=4, ensure_ascii=False)

    conn.close()
    print(f'Ranking was exported succesfully to {output_file}.')


load_dotenv()
db_path_env = os.getenv('DB_PATH')
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, db_path_env)
json_path = os.path.join(script_dir, '../data/player_ranking.json')
export_ranking_to_json(db_name=db_path, output_file=json_path)