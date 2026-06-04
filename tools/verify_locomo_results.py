#!/usr/bin/env python3
"""Verify saved LoCoMo result artifacts.

This script intentionally contains no PhasePrompt or LanguageWe implementation.
It only recomputes metrics from saved JSONL result files.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ORDER = ["NOCTX", "SUM_NONE", "SUM_REC", "SUM_LW", "SUM_HYB", "FULL"]


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def summarize(rows: list[dict], include_full: bool) -> None:
    by_cond: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_cond[row.get("condition", "")].append(row)

    print("Condition summary")
    print("-----------------")
    for cond in ORDER:
        if cond == "FULL" and not include_full:
            continue
        group = by_cond.get(cond, [])
        if not group:
            continue
        acc = sum(1 for r in group if r.get("accuracy") is True) / len(group)
        uniq_qids = len({r.get("qid") for r in group})
        print(f"{cond:<9} n={len(group):>4} unique_qid={uniq_qids:>4} acc={pct(acc):>6}")

    print()
    print("Input-token use")
    print("---------------")
    token_totals: dict[str, int] = {}
    for cond in ORDER:
        if cond == "FULL" and not include_full:
            continue
        group = by_cond.get(cond, [])
        if not group:
            continue
        total = sum(int(r.get("input_tokens") or 0) for r in group)
        avg = total / len(group)
        token_totals[cond] = total
        print(f"{cond:<9} total_input={total:>7} avg_input={avg:>6.1f}")
    if "SUM_REC" in token_totals and "SUM_LW" in token_totals:
        rec = token_totals["SUM_REC"]
        lw = token_totals["SUM_LW"]
        if rec:
            print(f"SUM_LW vs SUM_REC input saving: {rec - lw:,} tokens ({(rec - lw) / rec:.1%})")

    if "SUM_REC" in by_cond:
        print()
        print("Paired vs SUM_REC")
        print("-----------------")
        rec = {r.get("qid"): r.get("accuracy") is True for r in by_cond["SUM_REC"]}
        for cond in ["SUM_NONE", "SUM_LW", "SUM_HYB"]:
            if cond not in by_cond:
                continue
            cur = {r.get("qid"): r.get("accuracy") is True for r in by_cond[cond]}
            wins = losses = ties = 0
            for qid, value in cur.items():
                if qid not in rec:
                    continue
                if value and not rec[qid]:
                    wins += 1
                elif (not value) and rec[qid]:
                    losses += 1
                else:
                    ties += 1
            print(f"{cond:<9} {wins}W/{losses}L/{ties}T net={wins - losses:+d}")

    print()
    print("By question type")
    print("----------------")
    qtypes = sorted({r.get("question_type", "") for r in rows if r.get("question_type")})
    for qtype in qtypes:
        print(f"[{qtype}]")
        for cond in ["NOCTX", "SUM_NONE", "SUM_REC", "SUM_LW", "SUM_HYB"]:
            group = [
                r for r in by_cond.get(cond, [])
                if r.get("question_type") == qtype
            ]
            if not group:
                continue
            acc = sum(1 for r in group if r.get("accuracy") is True) / len(group)
            print(f"  {cond:<9} n={len(group):>3} acc={pct(acc):>6}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="result JSONL artifact")
    parser.add_argument("--full", action="store_true", help="include FULL rows if present")
    args = parser.parse_args()

    rows = load_jsonl(args.jsonl)
    if not rows:
        raise SystemExit(f"No rows loaded from {args.jsonl}")
    summarize(rows, include_full=args.full)


if __name__ == "__main__":
    main()
