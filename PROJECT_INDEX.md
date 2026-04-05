# Jellyfish Headless - 项目导航

## 快速导航

### 📖 核心文档

| 文档 | 描述 | 适合人群 |
|------|------|----------|
| [README.md](README.md) | 项目主页 | 所有人 |
| [DECOUPLING_SUMMARY.md](DECOUPLING_SUMMARY.md) | 解耦工作总结 | 了解项目全貌 |
| [jellyfish_video_flow.md](jellyfish_video_flow.md) | 视频流程图（8个子流程） | 架构师、开发者 |
| [SCRIPT_PROCESSING_ANALYSIS.md](SCRIPT_PROCESSING_ANALYSIS.md) | 剧本处理深度解析 | 深入研究者 |

### 🚀 快速开始

| 文档 | 描述 | 适合人群 |
|------|------|----------|
| [HEADLESS_GUIDE.md](HEADLESS_GUIDE.md) | CLI 工具使用指南 | 命令行用户 |
| [backend/STANDALONE_README.md](backend/STANDALONE_README.md) | 独立处理器使用指南 | Python 开发者 |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | 实现总结 | 技术人员 |

### 💻 代码文件

| 文件 | 描述 | 代码量 |
|------|------|--------|
| [backend/cli.py](backend/cli.py) | CLI 工具主程序 | 300+ 行 |
| [backend/script_processors_standalone.py](backend/script_processors_standalone.py) | 独立处理器 | 600+ 行 |
| [backend/test_processors.py](backend/test_processors.py) | 测试框架 | 500+ 行 |
| [backend/example_usage.py](backend/example_usage.py) | 使用示例 | 300+ 行 |

## 使用场景指南

### 场景1: 我想快速了解 Jellyfish 的架构

1. 阅读 [jellyfish_video_flow.md](jellyfish_video_flow.md) - 查看总体架构图
2. 阅读 [DECOUPLING_SUMMARY.md](DECOUPLING_SUMMARY.md) - 了解核心组件

### 场景2: 我想使用 CLI 工具处理剧本

1. 阅读 [HEADLESS_GUIDE.md](HEADLESS_GUIDE.md) - 学习 CLI 使用
2. 运行 `python3 backend/cli.py --help` - 查看命令帮助
3. 准备 `.env` 文件配置 LLM API

### 场景3: 我想独立测试剧本处理功能

1. 阅读 [backend/STANDALONE_README.md](backend/STANDALONE_README.md)
2. 运行 `python3 backend/test_processors.py` - 查看测试结果
3. 运行 `python3 backend/example_usage.py` - 查看使用示例

### 场景4: 我想集成到自己的项目

1. 复制 `backend/script_processors_standalone.py` 到你的项目
2. 实现 LLM 调用函数: `def my_llm(prompt: str) -> str`
3. 使用处理器: `processor.process(my_llm, script_text="...")`

### 场景5: 我想深入研究剧本处理算法

1. 阅读 [SCRIPT_PROCESSING_ANALYSIS.md](SCRIPT_PROCESSING_ANALYSIS.md)
2. 查看 [backend/script_processors_standalone.py](backend/script_processors_standalone.py) 源码
3. 研究 Prompt 设计和输出解析逻辑

## 核心功能速查

### 剧本处理流程

```
原始剧本 → 精简 → 一致性检查 → 优化 → 分镜
```

**处理器**:
- `ScriptSimplifier` - 精简剧本
- `ConsistencyChecker` - 检查角色混淆
- `ScriptOptimizer` - 修复问题
- `ScriptDivider` - 智能分镜

### CLI 命令

```bash
# 完整流程
python3 backend/cli.py process script.txt

# 单步处理
python3 backend/cli.py simplify script.txt
python3 backend/cli.py check script.txt
python3 backend/cli.py divide script.txt
```

### Python API

```python
from script_processors_standalone import ScriptDivider

divider = ScriptDivider()
result = divider.process(llm_func, script_text="剧本...")

for shot in result.shots:
    print(f"{shot.index}. {shot.shot_name}")
```

## 技术栈

### 原 Jellyfish 项目
- 前端: React 18 + TypeScript + Vite
- 后端: FastAPI + SQLAlchemy
- 数据库: MySQL
- 存储: RustFS/S3
- AI: LangChain + 多模型

### Headless 版本
- 语言: Python 3.10+
- 依赖: 标准库 + LLM SDK
- 架构: 解耦、模块化
- 测试: 内置测试框架

## 项目统计

### 代码规模
- 核心代码: 1700+ 行
- 测试代码: 500+ 行
- 文档: 3000+ 行

### 功能覆盖
- ✓ 剧本精简
- ✓ 一致性检查
- ✓ 剧本优化
- ✓ 智能分镜
- ✓ CLI 工具
- ✓ 独立测试

### 测试覆盖
- 单元测试: 9个
- 集成测试: 1个
- 通过率: 90%

## 贡献指南

### 报告问题
在 [GitHub Issues](https://github.com/joyhpc/jellyfish-headless/issues) 提交

### 提交代码
1. Fork 项目
2. 创建分支: `git checkout -b feature/your-feature`
3. 提交代码: `git commit -m "[feat] Your feature"`
4. 推送分支: `git push origin feature/your-feature`
5. 创建 Pull Request

### 提交规范
```
[feat] 新功能
[fix] Bug 修复
[docs] 文档更新
[test] 测试相关
[refactor] 重构
```

## 相关链接

- [Jellyfish 原项目](https://github.com/Forget-C/Jellyfish)
- [Jellyfish 官网](https://forget-c.github.io/Jellyfish)
- [本项目 GitHub](https://github.com/joyhpc/jellyfish-headless)

## 许可证

Apache-2.0

## 更新日志

### 2026-04-05
- ✓ 添加视频流程完整解析（8个子流程图）
- ✓ 实现独立剧本处理器（1400+ 行）
- ✓ 构建完整测试框架（90% 通过率）
- ✓ 提供多种 LLM 适配器
- ✓ 编写完整文档

### 2026-04-04
- ✓ 创建 Headless CLI 工具
- ✓ 实现基础剧本处理流程
- ✓ 添加使用指南

## 联系方式

- GitHub: [@joyhpc](https://github.com/joyhpc)
- 项目: [jellyfish-headless](https://github.com/joyhpc/jellyfish-headless)

---

**最后更新**: 2026-04-05
