"""
Generischer Export-Runner: führt Query aus, wendet optional einen
Processor an, schreibt JSON. Kein Job-spezifischer Code hier.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from db_utils import get_connection

Processor = Callable[[list[dict[str, Any]]], list[dict[str, Any]] | dict[str, Any]]
QueryFunc = Callable[..., tuple[str, tuple]]


@dataclass
class ExportJob:
    """Beschreibt einen einzelnen Export-Vorgang."""

    name: str  # sprechender Name fürs Logging
    query_func: QueryFunc  # Funktion aus queries/, gibt (sql, params) zurück
    output_file: str  # Dateiname, z.B. "total_ranking.json"
    query_args: tuple = field(default_factory=tuple)  # Positional-Args für query_func
    query_kwargs: dict = field(default_factory=dict)  # Keyword-Args für query_func
    processor: Processor | None = None  # optionale Nachbearbeitung
    active: bool = True  # Job überspringbar ohne Löschen


def run_job(job: ExportJob, output_dir: Path, verbose: bool = True) -> None:
    """Führt einen einzelnen ExportJob aus und schreibt das Ergebnis als JSON."""
    if not job.active:
        if verbose:
            print(f"⏭  {job.name} (inaktiv, übersprungen)")
        return

    sql, params = job.query_func(*job.query_args, **job.query_kwargs)

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()

    data: list[dict] | dict = job.processor(rows) if job.processor else rows

    output_path = output_dir / job.output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    if verbose:
        count = len(data) if isinstance(data, list) else 1
        print(f"✓  {job.name} → {job.output_file} ({count} Einträge)")


def run_jobs(jobs: list[ExportJob], output_dir: Path, verbose: bool = True) -> None:
    """Führt alle Jobs einer Liste aus."""
    for job in jobs:
        try:
            run_job(job, output_dir, verbose)
        except Exception as e:
            print(f"✗  {job.name} fehlgeschlagen: {e}")
