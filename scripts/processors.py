from typing import List, Dict, Any


def prepare_chart_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Converts data into chart.js compatible data.
    """
    chart_data = []
    for row in data:
        chart_data.append(
            {
                "label": row["label"],
                "data": [int(x) for x in row["data"].split(",")],
            }
        )
    return chart_data
