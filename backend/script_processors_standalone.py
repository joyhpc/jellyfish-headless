"""
独立的剧本处理器 - 解耦版本
无需 LangChain 依赖，可独立测试
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, TypeVar, Generic
import json
import re
from dataclasses import dataclass

T = TypeVar('T')


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class SimplificationResult:
    """精简结果"""
    simplified_script_text: str
    simplification_summary: str


@dataclass
class ConsistencyIssue:
    """一致性问题"""
    issue_type: str
    character_candidates: list[str]
    description: str
    suggestion: str
    affected_lines: Dict[str, int] | None = None
    evidence: list[str] | None = None


@dataclass
class ConsistencyCheckResult:
    """一致性检查结果"""
    has_issues: bool
    issues: list[ConsistencyIssue]
    summary: str | None = None


@dataclass
class OptimizationResult:
    """优化结果"""
    optimized_script_text: str
    change_summary: str


@dataclass
class ShotDivision:
    """单个镜头"""
    index: int
    start_line: int
    end_line: int
    shot_name: str
    script_excerpt: str
    time_of_day: str | None = None


@dataclass
class DivisionResult:
    """分镜结果"""
    total_shots: int
    shots: list[ShotDivision]
    notes: str | None = None


# ============================================================================
# 工具函数
# ============================================================================

def extract_json_from_text(raw: str) -> str:
    """从文本中提取 JSON"""
    text = raw.strip()
    # 尝试提取 markdown 代码块
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    return text


def repair_json(text: str) -> str:
    """修复常见的 JSON 格式问题"""
    repaired = text.strip()
    # 替换中文引号
    repaired = repaired.replace(""", '"').replace(""", '"')
    repaired = repaired.replace("'", "'").replace("'", "'")
    # 去除尾逗号
    repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
    return repaired


def parse_json_safe(text: str) -> Dict[str, Any]:
    """安全解析 JSON"""
    json_str = extract_json_from_text(text)
    json_str = repair_json(json_str)
    return json.loads(json_str)


# ============================================================================
# 处理器基类
# ============================================================================

class ScriptProcessor(ABC, Generic[T]):
    """剧本处理器基类"""

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass

    @abstractmethod
    def get_user_prompt(self, **kwargs) -> str:
        """获取用户提示词"""
        pass

    @abstractmethod
    def parse_output(self, raw_output: str) -> T:
        """解析 LLM 输出"""
        pass

    def process(self, llm_call: Callable[[str], str], **kwargs) -> T:
        """完整处理流程"""
        # 1. 构建提示词
        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(**kwargs)
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        # 2. 调用 LLM
        raw_output = llm_call(full_prompt)

        # 3. 解析输出
        return self.parse_output(raw_output)


# ============================================================================
# 1. 精简器
# ============================================================================

class ScriptSimplifier(ScriptProcessor[SimplificationResult]):
    """剧本精简器"""

    def get_system_prompt(self) -> str:
        return """你是"智能精简剧本Agent"。你的任务是：在不改变核心剧情走向的前提下精简剧本。

强约束：
- 必须保留剧情主体（关键事件、关键冲突、关键转折、结局/阶段性结果）。
- 必须保证剧情连续（时间顺序、因果关系、角色动机衔接不能断裂）。
- 禁止凭空新增关键设定或关键事件。
- 精简优先删除冗余重复描述、弱信息修饰、对主线无贡献的枝节句。
- 输出语言风格尽量贴近原文叙述口吻。

输出 JSON 格式：
{
    "simplified_script_text": "精简后的完整文本",
    "simplification_summary": "精简策略摘要（说明删改了什么、为何不影响主线）"
}

只输出 JSON。"""

    def get_user_prompt(self, script_text: str) -> str:
        return f"## 原文剧本\n{script_text}\n\n## 输出\n"

    def parse_output(self, raw_output: str) -> SimplificationResult:
        data = parse_json_safe(raw_output)

        # 字段兼容性处理
        simplified_text = data.get('simplified_script_text') or data.get('optimized_script_text', '')
        summary = data.get('simplification_summary') or data.get('change_summary', '')

        return SimplificationResult(
            simplified_script_text=simplified_text,
            simplification_summary=summary
        )


# ============================================================================
# 2. 一致性检查器
# ============================================================================

class ConsistencyChecker(ScriptProcessor[ConsistencyCheckResult]):
    """一致性检查器"""

    def get_system_prompt(self) -> str:
        return """你是"一致性检查员"。只做一件事：检测原文中是否把"同一个角色"在不同段落/镜头中赋予了不同的身份或行为主体，导致角色混淆（例如：同名不同人、代词指代混乱、行为归属错位）。

输出 JSON 格式：
{
    "has_issues": true/false,
    "issues": [
        {
            "issue_type": "character_confusion",
            "character_candidates": ["角色A", "角色B"],
            "description": "问题描述",
            "suggestion": "修改建议",
            "affected_lines": {"start_line": 10, "end_line": 15},
            "evidence": ["证据1", "证据2"]
        }
    ],
    "summary": "总结"
}

只输出 JSON。"""

    def get_user_prompt(self, script_text: str) -> str:
        return f"## 原文剧本\n{script_text}\n\n## 输出\n"

    def parse_output(self, raw_output: str) -> ConsistencyCheckResult:
        data = parse_json_safe(raw_output)

        issues = []
        for issue_data in data.get('issues', []):
            issues.append(ConsistencyIssue(
                issue_type=issue_data.get('issue_type', 'character_confusion'),
                character_candidates=issue_data.get('character_candidates', []),
                description=issue_data.get('description', ''),
                suggestion=issue_data.get('suggestion', ''),
                affected_lines=issue_data.get('affected_lines'),
                evidence=issue_data.get('evidence', [])
            ))

        return ConsistencyCheckResult(
            has_issues=data.get('has_issues', len(issues) > 0),
            issues=issues,
            summary=data.get('summary')
        )


# ============================================================================
# 3. 优化器
# ============================================================================

class ScriptOptimizer(ScriptProcessor[OptimizationResult]):
    """剧本优化器"""

    def get_system_prompt(self) -> str:
        return """你是"剧本优化师"。仅当一致性检查发现角色混淆问题时，对原文进行最小改写以消除混淆。

输入：
- script_text：原文
- consistency_json：一致性检查输出

输出 JSON 格式：
{
    "optimized_script_text": "优化后的完整剧本文本（尽量少改，只改与 issues 相关的段落）",
    "change_summary": "逐条对应 issues 的改动摘要"
}

只输出 JSON。"""

    def get_user_prompt(self, script_text: str, consistency_json: str) -> str:
        return f"## 一致性检查结果\n{consistency_json}\n\n## 原文剧本\n{script_text}\n\n## 输出\n"

    def parse_output(self, raw_output: str) -> OptimizationResult:
        data = parse_json_safe(raw_output)

        return OptimizationResult(
            optimized_script_text=data.get('optimized_script_text', ''),
            change_summary=data.get('change_summary', '')
        )


# ============================================================================
# 4. 分镜器
# ============================================================================

class ScriptDivider(ScriptProcessor[DivisionResult]):
    """剧本分镜器"""

    def get_system_prompt(self) -> str:
        return """你是"剧本分镜师"。将完整剧本分割为多个镜头。每个镜头应是完整的连贯场景。

为每个镜头提供：
- index（镜头序号，章节内唯一；从 1 开始）
- start_line、end_line
- shot_name（镜头名称/镜头标题，分镜名；一句话描述该镜头画面/动作；不要把它当作场景名）
- script_excerpt（镜头对应的剧本摘录/文本）
- time_of_day（时间段，如：黄昏、黎明、清晨等）

输出 JSON 格式：
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

只输出 JSON。"""

    def get_user_prompt(self, script_text: str) -> str:
        return f"## 输入脚本\n{script_text}\n\n## 输出\n"

    def parse_output(self, raw_output: str) -> DivisionResult:
        data = parse_json_safe(raw_output)

        # 处理多种可能的格式
        if isinstance(data, list):
            data = {"shots": data}
        elif "ScriptDivisionResult" in data:
            inner = data["ScriptDivisionResult"]
            if isinstance(inner, list):
                data = {"shots": inner}
            elif isinstance(inner, dict):
                data = inner

        shots = []
        for idx, shot_data in enumerate(data.get('shots', [])):
            if not isinstance(shot_data, dict):
                continue

            # 字段兼容性处理
            shot_name = shot_data.get('shot_name') or shot_data.get('title') or shot_data.get('shot_title', '')

            shots.append(ShotDivision(
                index=shot_data.get('index', idx + 1),
                start_line=shot_data.get('start_line', 0),
                end_line=shot_data.get('end_line', 0),
                shot_name=shot_name,
                script_excerpt=shot_data.get('script_excerpt', ''),
                time_of_day=shot_data.get('time_of_day')
            ))

        return DivisionResult(
            total_shots=data.get('total_shots', len(shots)),
            shots=shots,
            notes=data.get('notes')
        )


# ============================================================================
# 使用示例
# ============================================================================

def example_usage():
    """使用示例"""

    # 模拟 LLM 调用
    def mock_llm(prompt: str) -> str:
        if "精简" in prompt:
            return json.dumps({
                "simplified_script_text": "这是精简后的剧本",
                "simplification_summary": "删除了冗余描述"
            })
        elif "一致性" in prompt:
            return json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "未发现问题"
            })
        elif "分镜" in prompt:
            return json.dumps({
                "total_shots": 2,
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 10,
                        "shot_name": "开场",
                        "script_excerpt": "剧本片段1",
                        "time_of_day": "黄昏"
                    },
                    {
                        "index": 2,
                        "start_line": 11,
                        "end_line": 20,
                        "shot_name": "对话",
                        "script_excerpt": "剧本片段2",
                        "time_of_day": "夜晚"
                    }
                ]
            })
        return "{}"

    # 1. 精简剧本
    simplifier = ScriptSimplifier()
    result1 = simplifier.process(mock_llm, script_text="原始剧本...")
    print(f"精简结果: {result1.simplified_script_text}")

    # 2. 检查一致性
    checker = ConsistencyChecker()
    result2 = checker.process(mock_llm, script_text="剧本...")
    print(f"一致性检查: {result2.has_issues}")

    # 3. 分镜
    divider = ScriptDivider()
    result3 = divider.process(mock_llm, script_text="剧本...")
    print(f"分镜数量: {result3.total_shots}")
    for shot in result3.shots:
        print(f"  镜头 {shot.index}: {shot.shot_name}")


if __name__ == "__main__":
    example_usage()
