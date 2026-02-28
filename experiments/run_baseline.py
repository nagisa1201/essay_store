'''
Author: Nagisa 2964793117@qq.com
Date: 2026-02-28 18:05:21
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2026-02-28 22:07:40
FilePath: \essay_store\experiments\run_baseline.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from api_client import call_model


def load_samples(samples_file: Path):
    samples = []
    for line in samples_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        samples.append(json.loads(line))
    return samples


def main():
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root / ".env")

    samples_file = repo_root / "data" / "samples" / "samples.jsonl"
    output_file = repo_root / "results" / "baseline_outputs.jsonl"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    samples = load_samples(samples_file)
    print(f"Loaded {len(samples)} sample(s)")

    success_count = 0
    records = []
    with output_file.open("w", encoding="utf-8") as f:
        for sample in samples:
            image_path = repo_root / sample.get("image_path", "") if sample.get("image_path") else None
            try:
                result = call_model(
                    user_text=sample["text_prompt"],
                    image_path=image_path,
                )
                success_count += 1
                record = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "sample_id": sample["id"],
                    "input": sample,
                    "result": result,
                    "error": None,
                }
            except Exception as exc:
                record = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "sample_id": sample.get("id", "unknown"),
                    "input": sample,
                    "result": None,
                    "error": str(exc),
                }
            records.append(record)
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Finished. Success: {success_count}/{len(samples)}")
    print(f"Output written to: {output_file}")
    
    # 同时输出格式化 JSON 版本
    formatted_json_file = output_file.parent / "baseline_outputs_formatted.json"
    with formatted_json_file.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Formatted JSON written to: {formatted_json_file}")


if __name__ == "__main__":
    main()

