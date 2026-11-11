from pathlib import Path

from .analysis import summarize
from .clustering import cluster
from .preprocess import prepare
from .reports import write_reports


def main():
    project_dir = Path(__file__).resolve().parents[2]
    raw_data = project_dir / "data" / "raw" / "data.csv"
    processed_dir = project_dir / "output" / "processed"
    reports_dir = project_dir / "output" / "reports"

    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    features = prepare(raw_data, processed_dir)
    summarize(features, processed_dir)
    write_reports(processed_dir, reports_dir)
    cluster(processed_dir)
