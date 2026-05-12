#!/usr/bin/env python3
"""สคริปต์ตรวจสอบความพร้อมของไฟล์ watchlist.csv"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


# คอลัมน์ที่ต้องมีในไฟล์ watchlist.csv
REQUIRED_COLUMNS = [
    "ticker",
    "market",
    "name",
    "asset_type",
    "category",
    "risk_level",
    "priority",
    "reason_to_watch",
    "source_to_check",
    "note",
]


# ตำแหน่งไฟล์ watchlist.csv (อยู่ที่ root ของโปรเจกต์)
WATCHLIST_PATH = Path(__file__).resolve().parent.parent / "watchlist.csv"


def load_watchlist(path: Path) -> tuple[list[dict[str, str]], list[str], list[str]]:
    """อ่านไฟล์ CSV และคืนค่า rows, fieldnames และรายการคำเตือน"""
    warnings: list[str] = []

    if not path.exists():
        warnings.append(f"คำเตือน: ไม่พบไฟล์ {path.name}")
        return [], [], warnings

    with path.open("r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    return rows, fieldnames, warnings


def validate_columns(fieldnames: list[str]) -> list[str]:
    """ตรวจสอบว่าคอลัมน์ครบตามที่กำหนดหรือไม่"""
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in fieldnames]
    if not missing_cols:
        return []
    return [f"คำเตือน: คอลัมน์ขาดหาย: {', '.join(missing_cols)}"]


def validate_required_values(rows: list[dict[str, str]]) -> list[str]:
    """ตรวจสอบทุกแถวว่ามีค่า ticker และ market"""
    warnings: list[str] = []

    for idx, row in enumerate(rows, start=2):
        ticker = (row.get("ticker") or "").strip()
        market = (row.get("market") or "").strip()

        if not ticker and not market:
            warnings.append(f"คำเตือน: แถวที่ {idx} ไม่มีทั้ง ticker และ market")
        elif not ticker:
            warnings.append(f"คำเตือน: แถวที่ {idx} ไม่มี ticker")
        elif not market:
            warnings.append(f"คำเตือน: แถวที่ {idx} ไม่มี market")

    return warnings


def print_summary(rows: list[dict[str, str]]) -> None:
    """แสดงสรุปจำนวนข้อมูลทั้งหมด และแยกตาม market/asset_type"""
    total_count = len(rows)
    market_counter = Counter((row.get("market") or "").strip() for row in rows)
    asset_counter = Counter((row.get("asset_type") or "").strip() for row in rows)

    print(f"จำนวนหุ้น/ETF ทั้งหมด: {total_count}")

    print("\nจำนวนแยกตาม market:")
    for market, count in sorted(market_counter.items()):
        label = market or "(ว่าง)"
        print(f"- {label}: {count}")

    print("\nจำนวนแยกตาม asset_type:")
    for asset_type, count in sorted(asset_counter.items()):
        label = asset_type or "(ว่าง)"
        print(f"- {label}: {count}")


def main() -> None:
    """จุดเริ่มต้นของโปรแกรม"""
    rows, fieldnames, warnings = load_watchlist(WATCHLIST_PATH)

    if fieldnames:
        warnings.extend(validate_columns(fieldnames))

    if rows:
        warnings.extend(validate_required_values(rows))

    print_summary(rows)

    if warnings:
        print("\nผลการตรวจสอบ:")
        for message in warnings:
            print(message)
    else:
        print("\nwatchlist.csv พร้อมใช้งาน")


if __name__ == "__main__":
    main()
