import csv
import io
import tomllib
from pathlib import Path

import requests

with Path("src/task5/config/config.toml").open("rb") as f:
    cfg = tomllib.load(f)
    cell_range = cfg["spreadsheet"]["cell_range"]
    sheet_id = cfg["spreadsheet"]["sheet_id"]


def read_sheet_rows(sheet_id: str, gid: int = 0, cell_range: str = "A1:H15"):
    resp = requests.get(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export",
        params={"format": "csv", "gid": gid, "range": cell_range},
        timeout=30,
    )
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return list(csv.reader(io.StringIO(resp.text)))


def get_data_from_spreadhseet():
    try:
        data = read_sheet_rows(sheet_id=sheet_id, cell_range=cell_range)
    except Exception as error:
        print(f"Failed to fetch data: {error}")
    return data