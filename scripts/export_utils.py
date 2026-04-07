import json
from typing import Callable, List, Dict, Any


def export_to_json(data: List[Dict[str, Any]], output_path: str) -> None:
    """Export data as json."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def export_chart_data(data: List[Dict[str, Any]], output_path: str) -> None:
    """Export data ready for chart.js."""
    chart_data = []
    for row in data:
        label = row["label"]
        data_str = row["data"]
        data_points = [int(point) for point in data_str.split(", ")]
        chart_data.append({"label": label, "data": data_points, "fill": False})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chart_data, f, indent=4, ensure_ascii=False)


def process_and_export(
    db_path: str,
    query: str,
    processor: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]],
    output_path: str,
) -> None:
    """
    Excecutes a query, processes the returned data with a custom function and exports the result as JSON.

    Args:
        db_path: path to database.
        query: SQL-query.
        processor: function, that processes the raw data.
        output_path: path for the returned JSON-file.
    """
    from db_utils import execute_query

    raw_data = execute_query(db_path, query)
    processed_data = processor(raw_data)
    export_to_json(processed_data, output_path)
