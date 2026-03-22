from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


@dataclass
class MachineConfig:
    machine_id: str = "MACHINE_01"
    shift_hours: int = 8
    ideal_units_per_min: int = 10
    scrap_rate_run: float = 0.03
    random_stop_prob: float = 0.03
    random_fault_prob: float = 0.015


def choose_mode() -> None:
    print("\nSelect simulation mode:")
    print("1) Replicable (same data every run)")
    print("2) Variable (different data every run)")

    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()

        if choice == "1":
            random.seed(42)
            print("\nMode selected: REPLICABLE (fixed seed = 42)")
            break

        if choice == "2":
            random.seed()
            print("\nMode selected: VARIABLE (different output at each run)")
            break

        print("Invalid choice. Please enter 1 or 2.")


def simulate_it_metrics() -> dict:
    cpu = random.randint(35, 98)
    ram = random.randint(40, 92)
    network_ok = random.random() > 0.04
    service_ok = random.random() > 0.03

    return {
        "cpu_percent": cpu,
        "ram_percent": ram,
        "network_ok": network_ok,
        "service_ok": service_ok,
    }


def determine_state(metrics: dict, config: MachineConfig) -> tuple[str, str]:
    if not metrics["network_ok"]:
        return "STOP", "NETWORK_DOWN"

    if not metrics["service_ok"]:
        return "FAULT", "SERVICE_DOWN"

    roll = random.random()

    if roll < config.random_fault_prob:
        return "FAULT", "RANDOM_FAULT"

    if roll < config.random_fault_prob + config.random_stop_prob:
        return "STOP", "MINOR_STOP"

    return "RUN", "NORMAL_OPERATION"


def compute_performance_factor(cpu_percent: int) -> float:
    if cpu_percent > 90:
        return 0.60
    if cpu_percent > 85:
        return 0.75
    if cpu_percent > 75:
        return 0.90
    return 1.00


def simulate_shift(config: MachineConfig) -> pd.DataFrame:
    total_minutes = config.shift_hours * 60
    start_time = datetime.now().replace(second=0, microsecond=0)

    records = []

    for minute in range(total_minutes):
        timestamp = start_time + timedelta(minutes=minute)
        metrics = simulate_it_metrics()
        state, stop_reason = determine_state(metrics, config)

        produced_units = 0
        good_units = 0
        scrap_units = 0
        downtime_min = 0
        performance_factor = compute_performance_factor(metrics["cpu_percent"])

        if state == "RUN":
            produced_units = max(
                0,
                int(config.ideal_units_per_min * performance_factor + random.randint(-1, 1))
            )

            scrap_units = sum(
                1 for _ in range(produced_units)
                if random.random() < config.scrap_rate_run
            )

            good_units = produced_units - scrap_units
        else:
            downtime_min = 1

        records.append(
            {
                "timestamp": timestamp,
                "machine_id": config.machine_id,
                "state": state,
                "stop_reason": stop_reason,
                "cpu_percent": metrics["cpu_percent"],
                "ram_percent": metrics["ram_percent"],
                "network_ok": metrics["network_ok"],
                "service_ok": metrics["service_ok"],
                "produced_units": produced_units,
                "good_units": good_units,
                "scrap_units": scrap_units,
                "downtime_min": downtime_min,
                "ideal_units_per_min": config.ideal_units_per_min,
                "performance_factor": performance_factor,
            }
        )

    return pd.DataFrame(records)


def save_output(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def print_summary(df: pd.DataFrame) -> None:
    total_minutes = len(df)
    run_minutes = int((df["state"] == "RUN").sum())
    downtime_minutes = int(df["downtime_min"].sum())
    produced = int(df["produced_units"].sum())
    good = int(df["good_units"].sum())
    scrap = int(df["scrap_units"].sum())
    theoretical_output = int(df["ideal_units_per_min"].sum())

    availability = run_minutes / total_minutes if total_minutes else 0
    performance = produced / theoretical_output if theoretical_output else 0
    quality = good / produced if produced else 0
    oee = availability * performance * quality

    print("\n=== SHIFT SUMMARY ===")
    print(f"Total minutes:      {total_minutes}")
    print(f"Run minutes:        {run_minutes}")
    print(f"Downtime minutes:   {downtime_minutes}")
    print(f"Produced units:     {produced}")
    print(f"Good units:         {good}")
    print(f"Scrap units:        {scrap}")
    print(f"Availability:       {availability:.2%}")
    print(f"Performance:        {performance:.2%}")
    print(f"Quality:            {quality:.2%}")
    print(f"OEE:                {oee:.2%}")


def main() -> None:
    choose_mode()

    config = MachineConfig()
    df = simulate_shift(config)

    output_file = Path("data/production_data.csv")
    save_output(df, output_file)
    print_summary(df)
    print(f"\nCSV saved to: {output_file.resolve()}")


if __name__ == "__main__":
    main()
