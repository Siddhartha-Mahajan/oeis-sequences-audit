#!/usr/bin/env python3
"""Run the exact A003167(7) computation as disjoint prefix/range branches."""

from __future__ import annotations

import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    name: str
    args: tuple[int | str, ...]


def tasks() -> list[Task]:
    result = [Task(f"x{x}", (7, x)) for x in range(4, 15)]
    result += [Task(f"x3_y{y}", (7, 3, y)) for y in range(8, 37)]
    result += [Task(f"x3_y7_z{z}", (7, 3, 7, z)) for z in range(44, 211)]
    # For (3,7,43), the next denominator is in [1807,7224]. Splitting this
    # interval changes no count and makes the expensive exceptional branch
    # independently resumable.
    start = 1807
    while start <= 7224:
        width = 2 if start < 1827 else 10 if start < 2007 else 200
        end = min(7224, start + width - 1)
        result.append(
            Task(
                f"x3_y7_z43_w{start}_{end}",
                (7, 3, 7, 43, "--next-range", start, end),
            )
        )
        start = end + 1
    return result


def run(task: Task, binary: Path, output_dir: Path) -> tuple[str, str]:
    output = output_dir / f"{task.name}.txt"
    if output.exists() and output.stat().st_size:
        return task.name, "cached"
    completed = subprocess.run(
        [str(binary), *(str(value) for value in task.args)],
        check=True,
        capture_output=True,
        text=True,
    )
    output.write_text(completed.stdout, encoding="utf-8")
    if completed.stderr:
        (output_dir / f"{task.name}.stderr").write_text(
            completed.stderr, encoding="utf-8"
        )
    return task.name, "computed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, default=Path("scripts/count_pair_terminal_exact"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/n7_exact_v2"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    all_tasks = tasks()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run, task, args.binary, args.output_dir) for task in all_tasks]
        for index, future in enumerate(as_completed(futures), 1):
            name, status = future.result()
            print(f"[{index}/{len(all_tasks)}] {name}: {status}", flush=True)


if __name__ == "__main__":
    main()
