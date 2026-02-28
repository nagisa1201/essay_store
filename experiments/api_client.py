'''
Author: Nagisa 2964793117@qq.com
Date: 2026-02-28 18:05:21
LastEditors: Nagisa 2964793117@qq.com
LastEditTime: 2026-02-28 22:17:13
FilePath: \essay_store\experiments\api_client.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import os
import base64
from pathlib import Path
from typing import Any, Dict, Optional
from openai import OpenAI

SYSTEM_PROMPT = """
你是焊接实验助手。输入是文本任务描述，可能包含一张现场图片。
请仅输出一个JSON对象，必须包含以下字段：
1) task_summary: 字符串
2) recommended_parameters: 对象（包含你建议的关键参数）
3) skill_calls: 数组（每项包含 name 与 args）
4) risk_notes: 字符串数组

要求：
- 输出必须是合法JSON，不要输出Markdown代码块。
- 对不确定信息请在risk_notes中说明。
""".strip()


def call_model(
    user_text: str,
    image_path: Optional[Path] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 700,
) -> Dict[str, Any]:
    provider = os.getenv("LLM_PROVIDER", "iflow").strip().lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("缺少 OPENAI_API_KEY，请先在 .env 中配置。")
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    else:
        api_key = os.getenv("IFLOW_API_KEY")
        if not api_key:
            raise ValueError("缺少 IFLOW_API_KEY，请先在 .env 中配置。")
        base_url = os.getenv("IFLOW_BASE_URL", "https://apis.iflow.cn/v1")
        selected_model = model or os.getenv("IFLOW_MODEL", "deepseek-v3.1")

    client = OpenAI(api_key=api_key, base_url=base_url)

    user_content = [{"type": "text", "text": user_text}]

    if image_path and image_path.exists():
        suffix = image_path.suffix.lower().replace(".", "") or "jpeg"
        if suffix == "jpg":
            suffix = "jpeg"
        image_bytes = image_path.read_bytes()
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        user_content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/{suffix};base64,{encoded}"},
            }
        )

    raw_text = "{}"
    usage = {}
    try:
        completion = client.chat.completions.create(
            model=selected_model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
        raw_text = completion.choices[0].message.content or "{}"
        usage = completion.usage.model_dump() if completion.usage else {}
    except Exception as e:
        raw_text = f'{{"error": "{str(e)}"}}'

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = {
            "task_summary": "模型未返回合法JSON",
            "recommended_parameters": {},
            "skill_calls": [],
            "risk_notes": ["请检查提示词与模型响应格式"],
            "raw": raw_text,
        }

    return {
        "provider": provider,
        "model": selected_model,
        "parsed": parsed,
        "raw_text": raw_text,
        "usage": usage,
        "image_used": bool(image_path and image_path.exists()),
    }

