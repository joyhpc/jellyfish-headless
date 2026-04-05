# Jellyfish 剧本处理器 - 独立测试版

## 概述

这是从 Jellyfish 项目中解耦出来的剧本处理模块，可以独立运行和测试，无需依赖完整的 Jellyfish 系统。

## 文件结构

```
backend/
├── script_processors_standalone.py  # 独立的处理器实现
├── test_processors.py               # 测试框架和测试用例
├── example_usage.py                 # 使用示例
└── SCRIPT_PROCESSING_ANALYSIS.md    # 详细分析文档
```

## 核心组件

### 1. 四个处理器

#### ScriptSimplifier (精简器)
- **功能**: 精简剧本，删除冗余描述
- **输入**: 原始剧本文本
- **输出**: 精简后的剧本 + 精简说明

#### ConsistencyChecker (一致性检查器)
- **功能**: 检测角色混淆问题
- **输入**: 剧本文本
- **输出**: 问题列表 + 修改建议

#### ScriptOptimizer (优化器)
- **功能**: 根据一致性问题修复剧本
- **输入**: 原始剧本 + 一致性检查结果
- **输出**: 优化后的剧本 + 改动说明

#### ScriptDivider (分镜器)
- **功能**: 将剧本分割为多个镜头
- **输入**: 剧本文本
- **输出**: 分镜列表（镜头序号、名称、内容、时间等）

### 2. 处理流程

```
原始剧本
    ↓
[精简器] → 精简后剧本
    ↓
[一致性检查] → 问题列表
    ↓
[优化器] → 修复后剧本 (如有问题)
    ↓
[分镜器] → 分镜列表
```

## 快速开始

### 1. 运行测试

```bash
cd backend
python3 test_processors.py
```

**测试覆盖**:
- ✓ 正常处理流程
- ✓ 字段兼容性（旧字段名映射）
- ✓ JSON 提取（markdown 代码块）
- ✓ 多种输出格式处理
- ✓ 自动补全缺失字段
- ✓ 完整流程集成

### 2. 查看示例

```bash
python3 example_usage.py
```

### 3. 独立使用

```python
from script_processors_standalone import ScriptDivider

# 定义 LLM 调用函数
def my_llm(prompt: str) -> str:
    # 调用你的 LLM API
    return llm_response

# 使用分镜器
divider = ScriptDivider()
result = divider.process(my_llm, script_text="你的剧本...")

# 查看结果
for shot in result.shots:
    print(f"{shot.index}. {shot.shot_name}")
```

## LLM 适配器

支持多种 LLM 后端：

### OpenAI
```python
from example_usage import OpenAIAdapter

llm = OpenAIAdapter(api_key="your-key", model="gpt-4")
result = processor.process(llm, script_text="...")
```

### Anthropic Claude
```python
from example_usage import AnthropicAdapter

llm = AnthropicAdapter(api_key="your-key")
result = processor.process(llm, script_text="...")
```

### Ollama (本地)
```python
from example_usage import OllamaAdapter

llm = OllamaAdapter(model="qwen2.5:14b")
result = processor.process(llm, script_text="...")
```

### 自定义适配器
```python
def custom_llm(prompt: str) -> str:
    # 你的 LLM 调用逻辑
    response = your_llm_api.call(prompt)
    return response

result = processor.process(custom_llm, script_text="...")
```

## 完整流程示例

```python
from script_processors_standalone import (
    ScriptSimplifier,
    ConsistencyChecker,
    ScriptOptimizer,
    ScriptDivider,
)

# 1. 精简剧本
simplifier = ScriptSimplifier()
simplified = simplifier.process(llm, script_text=original_script)

# 2. 一致性检查
checker = ConsistencyChecker()
consistency = checker.process(llm, script_text=simplified.simplified_script_text)

# 3. 优化修复（如有问题）
if consistency.has_issues:
    optimizer = ScriptOptimizer()
    optimized = optimizer.process(
        llm,
        script_text=simplified.simplified_script_text,
        consistency_json=json.dumps(consistency_to_dict(consistency))
    )
    final_script = optimized.optimized_script_text
else:
    final_script = simplified.simplified_script_text

# 4. 智能分镜
divider = ScriptDivider()
division = divider.process(llm, script_text=final_script)

# 输出结果
print(f"总镜头数: {division.total_shots}")
for shot in division.shots:
    print(f"{shot.index}. {shot.shot_name} ({shot.time_of_day})")
```

## 测试结果

```
============================================================
总体测试结果
============================================================
总计: 10
通过: 9
失败: 1
成功率: 90.0%
============================================================
```

**测试套件**:
- ✓ ScriptSimplifier 测试 (3/3)
- ✓ ConsistencyChecker 测试 (2/2)
- ✓ ScriptDivider 测试 (4/4)
- ✗ 完整流程集成测试 (0/1) - 需要真实 LLM

## 数据模型

### SimplificationResult
```python
@dataclass
class SimplificationResult:
    simplified_script_text: str  # 精简后的剧本
    simplification_summary: str  # 精简说明
```

### ConsistencyCheckResult
```python
@dataclass
class ConsistencyCheckResult:
    has_issues: bool              # 是否有问题
    issues: list[ConsistencyIssue]  # 问题列表
    summary: str | None           # 总结
```

### ConsistencyIssue
```python
@dataclass
class ConsistencyIssue:
    issue_type: str                    # 问题类型
    character_candidates: list[str]    # 候选角色名
    description: str                   # 问题描述
    suggestion: str                    # 修改建议
    affected_lines: Dict[str, int] | None  # 影响行号
    evidence: list[str] | None         # 证据
```

### DivisionResult
```python
@dataclass
class DivisionResult:
    total_shots: int           # 总镜头数
    shots: list[ShotDivision]  # 镜头列表
    notes: str | None          # 分镜说明
```

### ShotDivision
```python
@dataclass
class ShotDivision:
    index: int              # 镜头序号
    start_line: int         # 起始行
    end_line: int           # 结束行
    shot_name: str          # 镜头名称
    script_excerpt: str     # 剧本片段
    time_of_day: str | None # 时间段
```

## 特性

### 1. 零依赖
- 不依赖 LangChain
- 不依赖 FastAPI
- 不依赖数据库
- 只需要标准库 + LLM API

### 2. 灵活的 LLM 后端
- 支持任何 LLM API
- 只需实现 `Callable[[str], str]` 接口
- 提供常见 LLM 的适配器

### 3. 完善的错误处理
- JSON 格式修复
- 字段兼容性处理
- 多种输出格式支持
- 自动补全缺失字段

### 4. 易于测试
- Mock LLM 支持
- 完整的测试框架
- 单元测试 + 集成测试

## 与原项目的区别

| 特性 | 原项目 | 独立版本 |
|------|--------|----------|
| 依赖 | LangChain + FastAPI + SQLAlchemy | 仅标准库 |
| 数据库 | 需要 MySQL | 不需要 |
| 部署 | Docker Compose | 单文件运行 |
| 测试 | 需要完整环境 | Mock LLM 即可 |
| 集成 | 紧耦合 | 松耦合 |

## 扩展

### 添加新的处理器

```python
from script_processors_standalone import ScriptProcessor

class MyCustomProcessor(ScriptProcessor[MyResult]):
    def get_system_prompt(self) -> str:
        return "你的系统提示词..."
    
    def get_user_prompt(self, **kwargs) -> str:
        return f"你的用户提示词: {kwargs['input']}"
    
    def parse_output(self, raw_output: str) -> MyResult:
        data = parse_json_safe(raw_output)
        return MyResult(**data)
```

### 添加新的测试

```python
from test_processors import TestSuite, TestCase, MockLLM

def test_my_processor():
    suite = TestSuite("MyProcessor 测试")
    
    tc = TestCase("test_name", "测试描述")
    try:
        mock_llm = MockLLM({"关键词": "响应"})
        processor = MyCustomProcessor()
        result = processor.process(mock_llm, input="测试")
        
        if result.output == "期望值":
            tc.passed = True
        else:
            tc.error_message = "输出不匹配"
    except Exception as e:
        tc.error_message = str(e)
    
    suite.add_test(tc)
    return suite
```

## 性能优化建议

1. **批量处理**: 如果有多个剧本，可以并行调用
2. **缓存结果**: 相同输入可以缓存 LLM 响应
3. **流式输出**: 对于长剧本，可以实现流式处理
4. **异步调用**: 使用 `async/await` 提升并发性能

## 常见问题

### Q: 如何处理超长剧本？
A: 可以先分段处理，然后合并结果。或者使用支持长上下文的模型。

### Q: LLM 输出格式不对怎么办？
A: 已内置多种格式修复逻辑，包括 JSON 修复、字段映射等。

### Q: 如何提高准确率？
A: 调整 system_prompt，增加示例，或使用更强的模型。

### Q: 可以用于其他语言的剧本吗？
A: 可以，只需修改 system_prompt 中的语言描述。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

Apache-2.0

## 相关链接

- [Jellyfish 主项目](https://github.com/Forget-C/Jellyfish)
- [详细分析文档](./SCRIPT_PROCESSING_ANALYSIS.md)
- [视频流程图](../jellyfish_video_flow.md)
