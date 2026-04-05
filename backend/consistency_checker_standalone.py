"""
独立的一致性检查器 - 完全解耦版本
专注于角色混淆检测
"""

import json
import re
from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass, asdict


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class ConsistencyIssue:
    """单个一致性问题"""
    issue_type: str  # 固定为 "character_confusion"
    character_candidates: List[str]  # 涉及的角色候选
    description: str  # 问题描述
    suggestion: str  # 修改建议
    affected_lines: Optional[Dict[str, int]] = None  # 受影响的行号
    evidence: Optional[List[str]] = None  # 原文依据


@dataclass
class ConsistencyCheckResult:
    """一致性检查结果"""
    has_issues: bool  # 是否发现问题
    issues: List[ConsistencyIssue]  # 问题列表
    summary: Optional[str] = None  # 总结


# ============================================================================
# 工具函数
# ============================================================================

def extract_json_from_text(raw: str) -> str:
    """从文本中提取 JSON"""
    text = raw.strip()
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    return text


def repair_json(text: str) -> str:
    """修复常见的 JSON 格式问题"""
    repaired = text.strip()
    repaired = repaired.replace(""", '"').replace(""", '"')
    repaired = repaired.replace("'", "'").replace("'", "'")
    repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
    return repaired


def parse_json_safe(text: str) -> Dict[str, Any]:
    """安全解析 JSON"""
    json_str = extract_json_from_text(text)
    json_str = repair_json(json_str)
    return json.loads(json_str)


# ============================================================================
# 一致性检查器
# ============================================================================

class ConsistencyChecker:
    """独立的一致性检查器"""

    SYSTEM_PROMPT = """你是"一致性检查员"。只做一件事：检测原文中是否把"同一个角色"在不同段落/镜头中赋予了不同的身份或行为主体，导致角色混淆。

检查类型：
1. 同名不同人：同一名字指代不同角色
2. 代词指代混乱：他/她/它指代不明确
3. 行为归属错位：行为主体错误归属
4. 称呼不一致：同一角色有多种称呼导致混淆

输出 JSON 格式：
{
    "has_issues": true/false,
    "issues": [
        {
            "issue_type": "character_confusion",
            "character_candidates": ["角色A", "角色B"],
            "description": "问题描述（为什么会混淆）",
            "suggestion": "修改建议（如何改写以消除混淆）",
            "affected_lines": {"start_line": 10, "end_line": 15},
            "evidence": ["原文片段1", "原文片段2"]
        }
    ],
    "summary": "总结"
}

只输出 JSON。"""

    @staticmethod
    def get_user_prompt(script_text: str) -> str:
        """生成用户提示词"""
        return f"## 原文剧本\n{script_text}\n\n## 输出\n"

    @staticmethod
    def parse_output(raw_output: str) -> ConsistencyCheckResult:
        """解析 LLM 输出"""
        data = parse_json_safe(raw_output)

        # 规范化数据
        if "issues" not in data or not isinstance(data["issues"], list):
            data["issues"] = []

        # 解析问题列表
        issues = []
        for issue_data in data.get("issues", []):
            issues.append(ConsistencyIssue(
                issue_type=issue_data.get("issue_type", "character_confusion"),
                character_candidates=issue_data.get("character_candidates", []),
                description=issue_data.get("description", ""),
                suggestion=issue_data.get("suggestion", ""),
                affected_lines=issue_data.get("affected_lines"),
                evidence=issue_data.get("evidence", [])
            ))

        # 自动计算 has_issues
        has_issues = data.get("has_issues", len(issues) > 0)

        return ConsistencyCheckResult(
            has_issues=has_issues,
            issues=issues,
            summary=data.get("summary")
        )

    def check(
        self,
        script_text: str,
        llm_call: Callable[[str], str]
    ) -> ConsistencyCheckResult:
        """
        检查剧本一致性

        Args:
            script_text: 剧本文本
            llm_call: LLM 调用函数

        Returns:
            ConsistencyCheckResult
        """
        # 构建完整提示词
        full_prompt = f"{self.SYSTEM_PROMPT}\n\n{self.get_user_prompt(script_text)}"

        # 调用 LLM
        raw_output = llm_call(full_prompt)

        # 解析输出
        return self.parse_output(raw_output)


# ============================================================================
# 便捷函数
# ============================================================================

def check_consistency(
    script_text: str,
    llm_call: Callable[[str], str]
) -> Dict[str, Any]:
    """
    检查剧本一致性（便捷函数）

    Args:
        script_text: 剧本文本
        llm_call: LLM 调用函数

    Returns:
        字典格式的检查结果
    """
    checker = ConsistencyChecker()
    result = checker.check(script_text, llm_call)

    # 转换为字典
    return {
        "has_issues": result.has_issues,
        "issues": [asdict(issue) for issue in result.issues],
        "summary": result.summary
    }


# ============================================================================
# 使用示例
# ============================================================================

def example_usage():
    """使用示例"""

    # 模拟 LLM 调用
    def mock_llm(prompt: str) -> str:
        if "小王子" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["小王子", "男孩", "金发少年"],
                        "description": "同一角色在不同幕中使用了三种不同称呼，可能让读者误以为是不同角色",
                        "suggestion": "统一使用'小王子'作为主要称呼",
                        "affected_lines": {"start_line": 1, "end_line": 3},
                        "evidence": [
                            "第1幕: 小王子住在B612星球",
                            "第2幕: 男孩遇到了飞行员",
                            "第3幕: 金发少年说话"
                        ]
                    }
                ],
                "summary": "发现1个角色混淆问题，建议统一角色称呼"
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "未发现角色混淆问题"
            }, ensure_ascii=False)

    # 测试1: 有问题的剧本
    script1 = """
    第1幕: 小王子住在B612星球。
    第2幕: 男孩遇到了飞行员。
    第3幕: 金发少年说："请给我画一只羊。"
    """

    checker = ConsistencyChecker()
    result1 = checker.check(script1, mock_llm)

    print("测试1: 有问题的剧本")
    print(f"  发现问题: {result1.has_issues}")
    print(f"  问题数量: {len(result1.issues)}")
    if result1.issues:
        issue = result1.issues[0]
        print(f"  角色候选: {issue.character_candidates}")
        print(f"  问题描述: {issue.description}")
        print(f"  修改建议: {issue.suggestion}")

    # 测试2: 无问题的剧本
    script2 = """
    陆景琛是陆氏集团的总裁。
    林小暖是新来的实习生。
    陆景琛对林小暖说："你好。"
    """

    result2 = checker.check(script2, mock_llm)

    print("\n测试2: 无问题的剧本")
    print(f"  发现问题: {result2.has_issues}")
    print(f"  总结: {result2.summary}")


if __name__ == "__main__":
    example_usage()
