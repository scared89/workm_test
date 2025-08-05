import datetime
import json
from collections import defaultdict
from tabulate import tabulate
import argparse
from datetime import datetime
from typing import Optional


def is_valid_date(timestamp_str, filter_date):
    return datetime.fromisoformat(timestamp_str).date() == filter_date


def parse_files(filenames, filter_date: Optional[datetime.date] = None):
    stats = defaultdict(list)

    for filename in filenames:
        with open(filename) as f:
            for line in f:
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not filter_date or is_valid_date(data["@timestamp"], filter_date):
                    stats[data["url"]].append({
                        "response_time": data["response_time"],
                    })

    return stats


def generate_avg_report(stats: dict) -> list:
    rows = []
    for url, entries in stats.items():
        response_time = [entry["response_time"] for entry in entries]
        avg = round(sum(response_time) / len(response_time), 3)
        times = len(response_time)
        rows.append([url, times, avg])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", nargs="+", required=True)
    parser.add_argument("--report", choices=["average"], required=True)
    parser.add_argument("--date", required=False)
    args = parser.parse_args()

    filter_date = None
    if args.date:
        filter_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    stats = parse_files(args.file, filter_date)

    if args.report == "average":
        rows = generate_avg_report(stats)
        print(tabulate(rows, headers=["handler", "total", "avg_response_time"]))


if __name__ == "__main__":
    main()
