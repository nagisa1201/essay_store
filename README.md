# essay_store

论文存储仓库。

## 新增：LLM官方API最小科研实验（Python）

本仓库已加入一个“新手可跑通”的最小实验：

- 输入：文本 + 单张图片
- 输出：结构化焊接参数建议 + 技能调用列表

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 配置平台与密钥

复制 `.env.example` 为 `.env`。可二选一：

```bash
LLM_PROVIDER=iflow
IFLOW_API_KEY=your_iflow_api_key_here
IFLOW_MODEL=deepseek-v3.1
IFLOW_BASE_URL=https://apis.iflow.cn/v1
```

或使用 OpenAI 官方：

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3) 准备样本

- 将图片放在 `data/samples/images/`
- 修改 `data/samples/samples.jsonl` 中对应 `image_path`

### 4) 运行基线

```bash
python experiments/run_baseline.py
```

输出文件：`results/baseline_outputs.jsonl`

### 5) 运行评估

```bash
python experiments/evaluate_baseline.py
```

评估文件：`results/eval_report.json`

详细说明见：`docs/llm_quickstart.md`
