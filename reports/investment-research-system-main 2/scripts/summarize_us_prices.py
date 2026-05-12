"""สรุปราคาหุ้น/ETF สหรัฐจากไฟล์ CSV เป็นรายงาน Markdown ภาษาไทย

เงื่อนไขสำคัญ:
- อ่านข้อมูลจากไฟล์ใน data/prices/us/ เท่านั้น
- ไม่เรียก API ภายนอก
- คำนวณผลตอบแทนย้อนหลังโดยประมาณ 1M/3M/6M/1Y
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


DATA_DIR = Path("data/prices/us")
REPORT_PATH = Path("reports/us_price_summary.md")
PERIODS = {
    "1M": pd.DateOffset(months=1),
    "3M": pd.DateOffset(months=3),
    "6M": pd.DateOffset(months=6),
    "1Y": pd.DateOffset(years=1),
}


@dataclass
class TickerSummary:
    """เก็บผลลัพธ์สรุปของแต่ละ ticker"""

    ticker: str
    latest_date: pd.Timestamp
    latest_close: float
    returns: Dict[str, Optional[float]]
    strength_score: Optional[float]


def load_price_csv(file_path: Path) -> pd.DataFrame:
    """โหลด CSV ของราคาหุ้น และทำความสะอาดข้อมูลที่จำเป็น"""
    df = pd.read_csv(file_path)

    if "Date" not in df.columns or "Close" not in df.columns:
        raise ValueError(f"ไฟล์ {file_path} ไม่มีคอลัมน์ Date/Close ครบถ้วน")

    # แปลงชนิดข้อมูลให้พร้อมคำนวณ
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # ตัดแถวที่ข้อมูลหลักหาย
    df = df.dropna(subset=["Date", "Close"]).copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if df.empty:
        raise ValueError(f"ไฟล์ {file_path} ไม่มีข้อมูล Date/Close ที่ใช้งานได้")

    return df


def calc_return_since(df: pd.DataFrame, latest_date: pd.Timestamp, latest_close: float, offset: pd.DateOffset) -> Optional[float]:
    """คำนวณผลตอบแทนย้อนหลังแบบประมาณการ โดยหา close ล่าสุดที่ <= วันที่เป้าหมาย"""
    target_date = latest_date - offset
    hist = df[df["Date"] <= target_date]

    # ถ้าไม่มีข้อมูลก่อนวันเป้าหมาย จะคืน None
    if hist.empty:
        return None

    base_close = hist.iloc[-1]["Close"]
    if base_close == 0:
        return None

    return (latest_close / base_close) - 1


def summarize_ticker(file_path: Path) -> TickerSummary:
    """สรุปข้อมูล ticker เดียวจากไฟล์ CSV"""
    df = load_price_csv(file_path)

    latest_row = df.iloc[-1]
    latest_date = latest_row["Date"]
    latest_close = float(latest_row["Close"])

    returns: Dict[str, Optional[float]] = {}
    for label, offset in PERIODS.items():
        returns[label] = calc_return_since(df, latest_date, latest_close, offset)

    valid_returns = [r for r in returns.values() if r is not None]
    strength_score = sum(valid_returns) / len(valid_returns) if valid_returns else None

    return TickerSummary(
        ticker=file_path.stem.upper(),
        latest_date=latest_date,
        latest_close=latest_close,
        returns=returns,
        strength_score=strength_score,
    )


def pct_text(value: Optional[float]) -> str:
    """แปลงตัวเลขเป็นเปอร์เซ็นต์อ่านง่าย"""
    if value is None:
        return "N/A"
    return f"{value * 100:+.2f}%"


def build_markdown_report(summaries: List[TickerSummary]) -> str:
    """สร้างข้อความรายงาน Markdown ภาษาไทย"""
    today_str = pd.Timestamp.utcnow().strftime("%Y-%m-%d")

    ranked = [s for s in summaries if s.strength_score is not None]
    ranked.sort(key=lambda x: x.strength_score, reverse=True)

    strongest = ranked[:3]
    weakest = ranked[-3:] if ranked else []

    lines: List[str] = []
    lines.append("# สรุปราคาหุ้น/ETF สหรัฐ (จากไฟล์ CSV)")
    lines.append("")
    lines.append(f"อัปเดตรายงาน: {today_str}")
    lines.append("")

    lines.append("## TL;DR")
    if strongest:
        top_names = ", ".join(s.ticker for s in strongest)
        weak_names = ", ".join(s.ticker for s in weakest)
        lines.append(f"- กลุ่มที่เด่นตามผลตอบแทนย้อนหลังเฉลี่ย: **{top_names}**")
        lines.append(f"- กลุ่มที่อ่อนแรงตามผลตอบแทนย้อนหลังเฉลี่ย: **{weak_names}**")
    else:
        lines.append("- ข้อมูลยังไม่พอสำหรับจัดอันดับความแข็งแรง (อาจมีประวัติราคาสั้นเกินไป)")
    lines.append("- ผลลัพธ์นี้อิงข้อมูลในโฟลเดอร์ `data/prices/us/` เท่านั้น")
    lines.append("")

    lines.append("## ตารางสรุปแต่ละ ticker")
    lines.append("")
    lines.append("| Ticker | วันที่ล่าสุด | ราคาปิดล่าสุด | 1M | 3M | 6M | 1Y | คะแนนความแข็งแรง (เฉลี่ย) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for s in sorted(summaries, key=lambda x: x.ticker):
        lines.append(
            "| {ticker} | {date} | {close:.2f} | {r1} | {r3} | {r6} | {r1y} | {score} |".format(
                ticker=s.ticker,
                date=s.latest_date.strftime("%Y-%m-%d"),
                close=s.latest_close,
                r1=pct_text(s.returns["1M"]),
                r3=pct_text(s.returns["3M"]),
                r6=pct_text(s.returns["6M"]),
                r1y=pct_text(s.returns["1Y"]),
                score=pct_text(s.strength_score),
            )
        )
    lines.append("")

    lines.append("## หุ้น/ETF ที่แข็งแรง")
    if strongest:
        for idx, s in enumerate(strongest, start=1):
            lines.append(f"{idx}. **{s.ticker}** (คะแนนเฉลี่ย: {pct_text(s.strength_score)})")
    else:
        lines.append("- ไม่สามารถสรุปได้จากข้อมูลที่มี")
    lines.append("")

    lines.append("## หุ้น/ETF ที่อ่อนแอ")
    if weakest:
        for idx, s in enumerate(weakest, start=1):
            lines.append(f"{idx}. **{s.ticker}** (คะแนนเฉลี่ย: {pct_text(s.strength_score)})")
    else:
        lines.append("- ไม่สามารถสรุปได้จากข้อมูลที่มี")
    lines.append("")

    lines.append("## ข้อควรระวัง")
    lines.append("- ผลตอบแทนเป็นการคำนวณแบบประมาณจากราคาปิดล่าสุดเทียบกับราคาก่อนหน้าในอดีต")
    lines.append("- หากวันเป้าหมายตรงวันหยุด/ไม่มีข้อมูล ระบบจะใช้ข้อมูลวันก่อนหน้าที่ใกล้ที่สุด")
    lines.append("- บาง ticker อาจมีข้อมูลไม่ครบทุกช่วงเวลา ทำให้ค่า 1M/3M/6M/1Y เป็น N/A")
    lines.append("- การจัดอันดับความแข็งแรงใช้ค่าเฉลี่ยผลตอบแทนย้อนหลังที่มีอยู่ ไม่ได้สะท้อนความเสี่ยงทั้งหมด")
    lines.append("")

    lines.append("## Disclaimer")
    lines.append("รายงานนี้จัดทำเพื่อการวิเคราะห์ข้อมูลย้อนหลังเท่านั้น **ไม่ใช่คำแนะนำในการซื้อขายหลักทรัพย์**")
    lines.append("ผู้ใช้งานควรศึกษาข้อมูลเพิ่มเติมและพิจารณาความเสี่ยงก่อนตัดสินใจลงทุน")

    return "\n".join(lines)


def main() -> None:
    """อ่านไฟล์ CSV ทั้งหมดและเขียนรายงานสรุป"""
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"ไม่พบไฟล์ CSV ใน {DATA_DIR}")

    summaries: List[TickerSummary] = []
    errors: List[str] = []

    for file_path in csv_files:
        try:
            summaries.append(summarize_ticker(file_path))
        except Exception as exc:  # เก็บข้อผิดพลาดเป็นรายไฟล์เพื่อให้กระบวนการไม่ล้มทั้งชุด
            errors.append(f"- {file_path.name}: {exc}")

    if not summaries:
        raise RuntimeError("ไม่สามารถสรุปข้อมูลได้จากทุกไฟล์")

    report = build_markdown_report(summaries)
    if errors:
        report += "\n\n## หมายเหตุไฟล์ที่ประมวลผลไม่ได้\n" + "\n".join(errors) + "\n"

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"เขียนรายงานแล้ว: {REPORT_PATH}")


if __name__ == "__main__":
    main()
