import json
from pathlib import Path


REQUIRED_FIELDS = [
    "task_summary",
    "recommended_parameters",
    "skill_calls",
    "risk_notes",
]


def main():
    repo_root = Path(__file__).resolve().parents[1]
    results_file = repo_root / "results" / "baseline_outputs.jsonl"
    report_file = repo_root / "results" / "eval_report.json"

    if not results_file.exists():
        raise FileNotFoundError("未找到 baseline 输出，请先运行 experiments/run_baseline.py")

    total = 0
    ok = 0
    failed_ids = []

    for line in results_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        total += 1
        row = json.loads(line)
        if row.get("error"):
            failed_ids.append(row.get("sample_id"))
            continue

        parsed = ((row.get("result") or {}).get("parsed")) or {}
        if all(field in parsed for field in REQUIRED_FIELDS):
            ok += 1
        else:
            failed_ids.append(row.get("sample_id"))

    success_rate = (ok / total) if total else 0.0
    report = {
        "total_samples": total,
        "format_ok_samples": ok,
        "format_success_rate": round(success_rate, 4),
        "failed_sample_ids": failed_ids,
    }

    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Report written to: {report_file}")


if __name__ == "__main__":
    main()
