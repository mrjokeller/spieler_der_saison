from typing import List, Dict, Any


def prepare_chart_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts data into chart.js compatible data.
    """
    chart_data = []
    for row in data:
        print(row)
        chart_data.append(
            {
                "label": row["label"],
                "data": [int(x) for x in row["data"].split(",")],
            }
        )
    return chart_data

def longest_streak(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    streaks = []
    for row in data:
        points = [int(x.strip()) for x in row['data_points'].split(',')]

        max_streak = 0
        current_streak = 0
        previous_points = 0

        for point in points:
            if point > previous_points:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
            previous_points = point
        
        streaks.append(
            {
                'player_name': row['player_name'], 
                'longest_streak': max_streak
            }
        )
    
    return sorted(streaks, key=lambda x: x['longest_streak'], reverse=True)
