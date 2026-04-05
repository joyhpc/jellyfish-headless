# Jellyfish 无界面版本 - 使用指南

## 概述

Jellyfish 无界面版本是专为无界面 Ubuntu 服务器环境设计的 AI 短剧生产工具。通过命令行界面（CLI）提供完整的剧本处理功能。

## 快速开始

### 1. 环境准备

```bash
cd /home/ubuntu/jellyfish-headless/backend

# 安装依赖
uv sync

# 初始化数据库
uv run python init_db.py

# 初始化默认LLM配置
uv run python init_llm.py
```

### 2. 配置 API Key

编辑 `.env` 文件，添加你的 OpenAI API Key：

```bash
# 方式1: 直接编辑 .env
echo "OPENAI_API_KEY=sk-your-actual-key-here" >> .env

# 方式2: 或者使用 SQLite 直接修改数据库
sqlite3 jellyfish.db "UPDATE providers SET api_key='sk-your-actual-key-here' WHERE name='OpenAI';"
```

### 3. 测试连接

```bash
uv run python cli.py test-connection
```

预期输出：
```
测试数据库连接...
✓ 数据库连接成功

测试LLM连接...
✓ LLM配置加载成功

✓ 基础环境检查通过
```

## CLI 命令详解

### 查看帮助

```bash
uv run python cli.py --help
```

### 1. 剧本精简 (simplify)

将冗长的剧本精简为核心内容。

```bash
uv run python cli.py simplify script.txt -o simplified.json
```

**参数**：
- `script_file`: 输入剧本文件路径（必需）
- `-o, --output`: 输出 JSON 文件路径（可选）

**示例**：
```bash
# 精简剧本并保存
uv run python cli.py simplify /path/to/little_prince_act1.txt -o output/simplified.json

# 精简剧本并直接输出到终端
uv run python cli.py simplify script.txt
```

### 2. 剧本优化 (optimize)

优化剧本的叙事结构和语言表达。

```bash
uv run python cli.py optimize script.txt -o optimized.json
```

**参数**：
- `script_file`: 输入剧本文件路径（必需）
- `-o, --output`: 输出 JSON 文件路径（可选）

### 3. 一致性检查 (check-consistency)

检查剧本中的角色混淆和一致性问题。

```bash
uv run python cli.py check-consistency script.txt -o consistency.json
```

**参数**：
- `script_file`: 输入剧本文件路径（必需）
- `-o, --output`: 输出 JSON 文件路径（可选）

**输出示例**：
```
正在检查剧本一致性: script.txt
发现 2 个一致性问题:

问题 1:
  描述: 角色"小王子"在第10行被称为"男孩"，可能造成混淆
  影响行: 10-15
  建议: 统一使用"小王子"称呼

问题 2:
  描述: 飞行员的年龄描述前后不一致
  影响行: 20-25
  建议: 确认角色年龄设定
```

### 4. 智能分镜 (divide)

将剧本自动分割为多个镜头。

```bash
uv run python cli.py divide script.txt -o division.json
```

**参数**：
- `script_file`: 输入剧本文件路径（必需）
- `-o, --output`: 输出 JSON 文件路径（可选）
- `--chapter-id`: 章节 ID（写入数据库时必需）
- `--write-db`: 是否写入数据库（标志）

**示例**：
```bash
# 分镜并保存到文件
uv run python cli.py divide script.txt -o division.json

# 分镜并写入数据库
uv run python cli.py divide script.txt --chapter-id ch001 --write-db
```

**输出示例**：
```
正在分镜: script.txt
分镜完成，共 6 个镜头

分镜列表:
  镜头 1: 飞机坠机 (行 1-15)
  镜头 2: 飞行员困境 (行 16-30)
  镜头 3: 神秘声音 (行 31-40)
  镜头 4: 小王子登场 (行 41-60)
  镜头 5: 画羊尝试 (行 61-90)
  镜头 6: 箱子里的羊 (行 91-100)
```

### 5. 实体合并 (merge-entities)

合并多个镜头的实体提取结果。

```bash
uv run python cli.py merge-entities extractions.json -o merged.json
```

**参数**：
- `extractions_file`: 镜头提取结果 JSON 文件（必需）
- `-o, --output`: 输出 JSON 文件路径（可选）
- `--historical`: 历史实体库 JSON 文件（可选）
- `--division`: 分镜结果 JSON 文件（可选）

### 6. 完整处理流程 (process-full)

一键执行完整的剧本处理流程：精简 → 优化 → 一致性检查 → 分镜。

```bash
uv run python cli.py process-full script.txt -o ./output
```

**参数**：
- `script_file`: 输入剧本文件路径（必需）
- `-o, --output-dir`: 输出目录（默认：./output）

**输出结构**：
```
output/
├── 01_simplified.json    # 精简后的剧本
├── 02_optimized.json     # 优化后的剧本
├── 03_consistency.json   # 一致性检查结果
└── 04_division.json      # 分镜结果
```

**示例**：
```bash
uv run python cli.py process-full /path/to/little_prince_act1.txt -o ./little_prince_output
```

**输出示例**：
```
============================================================
开始完整处理流程
============================================================

[1/4] 精简剧本...
   精简完成，保存到: ./output/01_simplified.json

[2/4] 优化剧本...
   优化完成，保存到: ./output/02_optimized.json

[3/4] 检查一致性...
   未发现一致性问题，保存到: ./output/03_consistency.json

[4/4] 智能分镜...
   分镜完成，共 6 个镜头，保存到: ./output/04_division.json

============================================================
处理完成！
============================================================

所有结果已保存到: ./output
  - 精简剧本: 01_simplified.json
  - 优化剧本: 02_optimized.json
  - 一致性检查: 03_consistency.json
  - 分镜结果: 04_division.json (6 个镜头)
```

## 完整工作流示例

### 场景：处理《小王子》第一幕剧本

```bash
# 1. 准备剧本文件
cat > little_prince_act1.txt << 'EOF'
场景1：飞行员坠机

黄昏时分，撒哈拉沙漠。一架小型飞机拖着黑烟，在金色沙丘上空摇晃。
飞机迫降，扬起巨大沙尘。

飞行员从驾驶舱爬出，检查损坏的引擎。他满脸疲惫，汗水与沙尘混在一起。

飞行员（独白）："水只够一周...最近的绿洲在三百公里外。"

夜幕降临，满天繁星。飞行员坐在机翼下，借着手电筒修理引擎。

场景2：小王子登场

黎明前，一个轻柔的童声打破寂静。

小王子（画外音）："请你...给我画一只羊。"

飞行员惊醒，看到沙丘顶端站着一个小小的身影。
金色阳光从地平线升起，勾勒出小王子的轮廓。

小王子穿着绿色外套，金色头发，围着金色围巾。

小王子："请你...给我画一只羊。"
飞行员（惊讶）："什么？"
小王子（认真）："给我画一只羊。"
EOF

# 2. 执行完整处理流程
uv run python cli.py process-full little_prince_act1.txt -o ./little_prince_output

# 3. 查看分镜结果
cat ./little_prince_output/04_division.json | jq '.shots[] | {index, shot_name, lines: "\(.start_line)-\(.end_line)"}'

# 4. 如果需要写入数据库（假设已创建章节）
# 首先创建项目和章节（通过API或直接操作数据库）
# 然后执行：
uv run python cli.py divide little_prince_act1.txt --chapter-id <chapter_id> --write-db
```

## 输出格式说明

### JSON 输出结构

所有命令的 JSON 输出都遵循统一的结构：

#### 精简结果 (simplified.json)
```json
{
  "simplified_script": "精简后的剧本文本",
  "notes": "精简说明"
}
```

#### 优化结果 (optimized.json)
```json
{
  "optimized_script": "优化后的剧本文本",
  "notes": "优化说明"
}
```

#### 一致性检查结果 (consistency.json)
```json
{
  "has_issues": true,
  "issues": [
    {
      "description": "问题描述",
      "affected_lines": "10-15",
      "suggestion": "修改建议"
    }
  ],
  "summary": "总结"
}
```

#### 分镜结果 (division.json)
```json
{
  "total_shots": 6,
  "shots": [
    {
      "index": 1,
      "start_line": 1,
      "end_line": 15,
      "shot_name": "飞机坠机",
      "script_excerpt": "剧本片段...",
      "time_of_day": "黄昏"
    }
  ],
  "notes": "分镜说明"
}
```

## 故障排查

### 问题1: 数据库连接失败

```bash
# 检查数据库文件是否存在
ls -lh jellyfish.db

# 重新初始化数据库
uv run python init_db.py
```

### 问题2: LLM 配置失败

```bash
# 检查 .env 文件
cat .env | grep OPENAI_API_KEY

# 检查数据库中的配置
sqlite3 jellyfish.db "SELECT id, name, api_key FROM providers;"

# 重新初始化 LLM 配置
uv run python init_llm.py
```

### 问题3: 依赖缺失

```bash
# 重新同步依赖
uv sync

# 如果需要开发依赖
uv sync --group dev
```

### 问题4: 权限问题

```bash
# 确保 CLI 脚本有执行权限
chmod +x cli.py

# 确保数据库文件可写
chmod 644 jellyfish.db
```

## 性能优化建议

### 1. 批量处理

对于多个剧本文件，使用 shell 脚本批量处理：

```bash
#!/bin/bash
for script in scripts/*.txt; do
    basename=$(basename "$script" .txt)
    uv run python cli.py process-full "$script" -o "output/$basename"
done
```

### 2. 并行处理

使用 GNU parallel 并行处理多个文件：

```bash
find scripts/ -name "*.txt" | parallel -j 4 \
    'uv run python cli.py process-full {} -o output/{/.}'
```

### 3. 缓存优化

对于重复处理的剧本，可以缓存中间结果：

```bash
# 第一次处理
uv run python cli.py simplify script.txt -o cache/simplified.json

# 后续只处理后续步骤
uv run python cli.py optimize cache/simplified.json -o cache/optimized.json
```

## 与 API 服务集成

CLI 工具可以与后端 API 服务配合使用：

```bash
# 启动 API 服务（另一个终端）
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# 使用 CLI 处理剧本
uv run python cli.py process-full script.txt -o output/

# 通过 API 访问结果
curl http://localhost:8000/api/v1/studio/chapters
```

## 高级用法

### 自定义 LLM 模型

```bash
# 通过 SQLite 修改模型配置
sqlite3 jellyfish.db << EOF
UPDATE models 
SET name='gpt-4o', params='{"temperature": 0.7}' 
WHERE category='text';
EOF
```

### 导出为其他格式

```bash
# 将 JSON 结果转换为 Markdown
jq -r '.shots[] | "## 镜头 \(.index): \(.shot_name)\n\n\(.script_excerpt)\n"' \
    output/04_division.json > output/division.md
```

### 集成到 CI/CD

```yaml
# .github/workflows/process-scripts.yml
name: Process Scripts
on: [push]
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Process scripts
        run: |
          cd backend
          uv sync
          uv run python cli.py process-full scripts/script.txt -o output/
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: processed-scripts
          path: backend/output/
```

## 下一步

- 查看 [Jellyfish 视频流分析](../../VG/docs/jellyfish_video_flow_analysis.md) 了解完整工作流
- 查看 [场景4 Veo拆解方案](../../VG/docs/scene4_veo_breakdown.md) 了解视频生成流程
- 查看 [小王子第一幕剧本](../../VG/docs/little_prince_act1_script.md) 了解剧本格式

## 技术支持

- GitHub Issues: https://github.com/Forget-C/Jellyfish/issues
- 原项目文档: https://github.com/Forget-C/Jellyfish
