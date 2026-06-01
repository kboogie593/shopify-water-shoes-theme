#!/usr/bin/env python3
"""Model FurQuiet organic channel output against the $10K/month target."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "data" / "furquiet-channel-funnel-model.csv"
SESSION_COLUMNS = {
    "low": "Sessions Per Unit Low",
    "base": "Sessions Per Unit Base",
    "high": "Sessions Per Unit High",
}


@dataclass
class ChannelForecast:
    channel: str
    unit: str
    monthly_units: float
    sessions_per_unit: float
    sessions: float
    email_captures: float
    add_to_carts: float
    orders: float
    revenue: float
    revenue_per_unit: float
    units_for_target: float | None
    readiness_score: float
    constraint: str
    next_action: str


def parse_float(value: str) -> float:
    return float(value.strip().replace("%", "")) / (100 if value.strip().endswith("%") else 1)


def forecast_row(row: dict[str, str], mode: str, target: float) -> ChannelForecast:
    monthly_units = parse_float(row["Monthly Units"])
    sessions_per_unit = parse_float(row[SESSION_COLUMNS[mode]])
    sessions = monthly_units * sessions_per_unit
    email_captures = sessions * parse_float(row["Email Capture Rate"])
    add_to_carts = sessions * parse_float(row["Add To Cart Rate"])
    orders = sessions * parse_float(row["Order Conversion Rate"])
    revenue = orders * parse_float(row["AOV"])
    revenue_per_unit = revenue / monthly_units if monthly_units else 0.0
    units_for_target = target / revenue_per_unit if revenue_per_unit else None
    return ChannelForecast(
        channel=row["Channel"],
        unit=row["Primary Unit"],
        monthly_units=monthly_units,
        sessions_per_unit=sessions_per_unit,
        sessions=sessions,
        email_captures=email_captures,
        add_to_carts=add_to_carts,
        orders=orders,
        revenue=revenue,
        revenue_per_unit=revenue_per_unit,
        units_for_target=units_for_target,
        readiness_score=parse_float(row["Readiness Score"]),
        constraint=row["Main Constraint"],
        next_action=row["Next Action"],
    )


def load_forecasts(path: Path, mode: str, target: float) -> list[ChannelForecast]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return [forecast_row(row, mode, target) for row in reader]


def money(value: float) -> str:
    return f"${value:,.0f}"


def number(value: float) -> str:
    return f"{value:,.1f}" if value % 1 else f"{value:,.0f}"


def print_table(forecasts: list[ChannelForecast]) -> None:
    headers = ["Channel", "Units", "Sessions", "Emails", "ATC", "Orders", "Revenue"]
    rows = [
        [
            item.channel,
            number(item.monthly_units),
            number(item.sessions),
            number(item.email_captures),
            number(item.add_to_carts),
            number(item.orders),
            money(item.revenue),
        ]
        for item in forecasts
    ]
    widths = [
        max(len(str(row[index])) for row in [headers, *rows])
        for index in range(len(headers))
    ]
    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--mode", choices=sorted(SESSION_COLUMNS), default="base")
    parser.add_argument("--target", type=float, default=10_000)
    args = parser.parse_args()

    forecasts = load_forecasts(args.model, args.mode, args.target)
    total_sessions = sum(item.sessions for item in forecasts)
    total_emails = sum(item.email_captures for item in forecasts)
    total_atc = sum(item.add_to_carts for item in forecasts)
    total_orders = sum(item.orders for item in forecasts)
    total_revenue = sum(item.revenue for item in forecasts)
    gap = args.target - total_revenue

    print(f"FurQuiet organic funnel forecast ({args.mode})")
    print(f"Target: {money(args.target)} monthly revenue\n")
    print_table(forecasts)
    print()
    print(f"Total sessions: {number(total_sessions)}")
    print(f"Total email captures: {number(total_emails)}")
    print(f"Total add to carts: {number(total_atc)}")
    print(f"Total orders: {number(total_orders)}")
    print(f"Forecast revenue: {money(total_revenue)}")
    print(f"Gap to target: {money(max(gap, 0))}")

    print("\nHighest revenue per content unit:")
    for item in sorted(forecasts, key=lambda row: row.revenue_per_unit, reverse=True)[:3]:
        print(
            f"- {item.channel}: {money(item.revenue_per_unit)} per {item.unit}; "
            f"constraint: {item.constraint}"
        )

    print("\nNext execution priorities:")
    for item in sorted(forecasts, key=lambda row: row.revenue_per_unit * row.readiness_score, reverse=True)[:4]:
        print(f"- {item.channel}: {item.next_action}")

    if gap > 0:
        print("\nAdditional units needed to close the current gap:")
        for item in sorted(forecasts, key=lambda row: row.revenue_per_unit, reverse=True)[:4]:
            if item.revenue_per_unit:
                extra_units = gap / item.revenue_per_unit
                print(f"- {item.channel}: {number(extra_units)} more {item.unit.lower()}s/month")

        print("\nSingle-channel volume needed to close the full target:")
        for item in sorted(forecasts, key=lambda row: row.revenue_per_unit, reverse=True)[:4]:
            if item.units_for_target is not None:
                print(f"- {item.channel}: {number(item.units_for_target)} {item.unit.lower()}s/month")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
