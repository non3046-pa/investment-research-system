"""ดึงข้อมูลราคาหุ้นสหรัฐฯ จาก watchlist.csv แล้วบันทึกเป็นไฟล์ CSV แยกรายตัว

หมายเหตุ:
- สคริปต์นี้ใช้สำหรับดึงข้อมูลเพื่อการวิเคราะห์เท่านั้น
- ไม่มีการเชื่อมต่อระบบซื้อขาย และไม่มีการส่งคำสั่งซื้อขายใด ๆ
"""

from pathlib import Path

import pandas as pd
import yfinance as yf


WATCHLIST_PATH = Path("watchlist.csv")
OUTPUT_DIR = Path("data/prices/us")
REQUIRED_COLUMNS = {"ticker", "market"}


def load_us_tickers(watchlist_path: Path) -> list[str]:
    """อ่าน watchlist.csv และคืนรายชื่อ ticker ที่อยู่ในตลาด US เท่านั้น"""
    df = pd.read_csv(watchlist_path)

    # ตรวจสอบว่ามีคอลัมน์ขั้นต่ำที่ต้องใช้
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"watchlist.csv ไม่มีคอลัมน์ที่จำเป็น: {missing_cols}")

    # กรองเฉพาะตลาด US และตัดค่า ticker ที่ว่าง/ซ้ำ
    us_df = df[df["market"].astype(str).str.upper() == "US"]
    tickers = (
        us_df["ticker"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )
    return tickers


def fetch_and_save_one_year_history(ticker: str, output_dir: Path) -> bool:
    """ดึงข้อมูลย้อนหลัง 1 ปีของ ticker และบันทึกเป็น CSV

    คืนค่า True เมื่อสำเร็จ และ False เมื่อไม่สำเร็จ
    """
    try:
        # period='1y' คือข้อมูลย้อนหลังประมาณ 1 ปี
        history_df = yf.Ticker(ticker).history(period="1y")
    except Exception:
        # ข้อความเตือนภาษาไทยเมื่อเรียกข้อมูลไม่สำเร็จ
        print(f"[คำเตือน] ดึงข้อมูลของ {ticker} ไม่สำเร็จ (เกิดข้อผิดพลาดระหว่างเชื่อมต่อข้อมูล)")
        return False

    if history_df.empty:
        print(f"[คำเตือน] ดึงข้อมูลของ {ticker} ไม่สำเร็จ (ไม่พบข้อมูลย้อนหลัง 1 ปี)")
        return False

    output_path = output_dir / f"{ticker}.csv"
    history_df.to_csv(output_path)
    print(f"บันทึกข้อมูล {ticker} เรียบร้อย -> {output_path}")
    return True


def main() -> None:
    # สร้างโฟลเดอร์ปลายทางอัตโนมัติหากยังไม่มี
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        tickers = load_us_tickers(WATCHLIST_PATH)
    except Exception as exc:
        print(f"[คำเตือน] อ่าน watchlist.csv ไม่สำเร็จ: {exc}")
        return

    if not tickers:
        print("[คำเตือน] ไม่พบ ticker ตลาด US ใน watchlist.csv")
        return

    success_count = 0
    for ticker in tickers:
        if fetch_and_save_one_year_history(ticker, OUTPUT_DIR):
            success_count += 1

    print(f"เสร็จสิ้น: สำเร็จ {success_count}/{len(tickers)} รายการ")


if __name__ == "__main__":
    main()
