# LLM官方API科研实验：新手快速跑通

这份指南对应一个最小实验：输入“文本 + 单张图片”，输出结构化焊接参数建议与技能调用列表。

## 1. 你会得到什么

- 一个可执行脚本：`experiments/run_baseline.py`
- 一个最小评估脚本：`experiments/evaluate_baseline.py`
- 一个结果文件：`results/baseline_outputs.jsonl`

## 2. 环境准备

1. 安装 Python 3.10+
2. 在项目根目录执行：
   - `pip install -r requirements.txt`
3. 复制 `.env.example` 为 `.env`，选择一个提供方：
    - 心流开放平台（推荐新手先用，OpenAI兼容）：
       - `LLM_PROVIDER=iflow`
       - `IFLOW_API_KEY=...`
       - `IFLOW_MODEL=deepseek-v3.1`
       - `IFLOW_BASE_URL=https://apis.iflow.cn/v1`
    - OpenAI 官方：
       - `LLM_PROVIDER=openai`
       - `OPENAI_API_KEY=...`
       - `OPENAI_MODEL=gpt-4.1-mini`
       - `OPENAI_BASE_URL=https://api.openai.com/v1`

## 3. 准备样本

1. 将测试图片放到 `data/samples/images/`
2. 修改 `data/samples/samples.jsonl` 中的 `image_path`
3. `text_prompt` 用你的实验描述替换即可

## 4. 运行实验

1. 执行：`python experiments/run_baseline.py`
2. 查看输出：`results/baseline_outputs.jsonl`

## 5. 评估输出格式稳定性

1. 执行：`python experiments/evaluate_baseline.py`
2. 查看评估：`results/eval_report.json`

## 6. 你需要理解的4个核心点

1. **System Prompt**：规定输出JSON结构，是“可控输出”的核心。
2. **多模态输入**：图片会被编码并随同文本一起发送给模型。
3. **结构化输出**：统一字段方便后续接技能库函数。
4. **最小评估**：先检查格式成功率，再做业务正确性评估。
