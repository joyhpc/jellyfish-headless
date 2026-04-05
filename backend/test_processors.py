"""
独立测试框架 - 用于测试剧本处理器
"""

import json
from typing import Dict, Any, Callable, List
from dataclasses import asdict
from script_processors_standalone import (
    ScriptSimplifier,
    ConsistencyChecker,
    ScriptOptimizer,
    ScriptDivider,
    SimplificationResult,
    ConsistencyCheckResult,
    OptimizationResult,
    DivisionResult,
)


# ============================================================================
# Mock LLM
# ============================================================================

class MockLLM:
    """模拟 LLM 调用"""

    def __init__(self, responses: Dict[str, str]):
        """
        responses: 关键词 -> 响应的映射
        当 prompt 包含关键词时，返回对应的响应
        """
        self.responses = responses
        self.call_history: List[str] = []

    def __call__(self, prompt: str) -> str:
        self.call_history.append(prompt)

        # 根据 prompt 中的关键词匹配响应
        for keyword, response in self.responses.items():
            if keyword in prompt:
                return response

        # 默认响应
        return json.dumps({"error": "No matching response"})

    def get_call_count(self) -> int:
        return len(self.call_history)

    def get_last_prompt(self) -> str:
        return self.call_history[-1] if self.call_history else ""


# ============================================================================
# 测试用例
# ============================================================================

class TestCase:
    """单个测试用例"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.passed = False
        self.error_message = ""
        self.actual_output = None
        self.expected_output = None

    def __repr__(self):
        status = "✓" if self.passed else "✗"
        return f"{status} {self.name}: {self.description}"


# ============================================================================
# 测试套件
# ============================================================================

class TestSuite:
    """测试套件"""

    def __init__(self, name: str):
        self.name = name
        self.test_cases: List[TestCase] = []

    def add_test(self, test_case: TestCase):
        self.test_cases.append(test_case)

    def run(self) -> Dict[str, Any]:
        """运行所有测试"""
        passed = sum(1 for tc in self.test_cases if tc.passed)
        total = len(self.test_cases)

        return {
            "suite_name": self.name,
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "test_cases": self.test_cases
        }

    def print_results(self):
        """打印测试结果"""
        results = self.run()

        print(f"\n{'=' * 60}")
        print(f"测试套件: {results['suite_name']}")
        print(f"{'=' * 60}")

        for tc in results['test_cases']:
            print(tc)
            if not tc.passed:
                print(f"  错误: {tc.error_message}")
                if tc.expected_output:
                    print(f"  期望: {tc.expected_output}")
                if tc.actual_output:
                    print(f"  实际: {tc.actual_output}")

        print(f"\n{'=' * 60}")
        print(f"总计: {results['total']} | 通过: {results['passed']} | 失败: {results['failed']}")
        print(f"{'=' * 60}\n")


# ============================================================================
# 测试: ScriptSimplifier
# ============================================================================

def test_simplifier():
    """测试精简器"""
    suite = TestSuite("ScriptSimplifier 测试")

    # 测试1: 正常精简
    tc1 = TestCase("normal_simplification", "正常精简流程")
    try:
        mock_llm = MockLLM({
            "精简": json.dumps({
                "simplified_script_text": "精简后的剧本",
                "simplification_summary": "删除了冗余描述"
            })
        })

        simplifier = ScriptSimplifier()
        result = simplifier.process(mock_llm, script_text="这是一个很长的剧本...")

        tc1.actual_output = asdict(result)
        tc1.expected_output = {
            "simplified_script_text": "精简后的剧本",
            "simplification_summary": "删除了冗余描述"
        }

        if result.simplified_script_text == "精简后的剧本":
            tc1.passed = True
        else:
            tc1.error_message = "输出不匹配"

    except Exception as e:
        tc1.error_message = str(e)

    suite.add_test(tc1)

    # 测试2: 字段兼容性（旧字段名）
    tc2 = TestCase("field_compatibility", "兼容旧字段名")
    try:
        mock_llm = MockLLM({
            "精简": json.dumps({
                "optimized_script_text": "精简剧本",  # 旧字段名
                "change_summary": "说明"  # 旧字段名
            })
        })

        simplifier = ScriptSimplifier()
        result = simplifier.process(mock_llm, script_text="测试剧本")

        tc2.actual_output = asdict(result)

        if result.simplified_script_text == "精简剧本" and result.simplification_summary == "说明":
            tc2.passed = True
        else:
            tc2.error_message = "字段映射失败"

    except Exception as e:
        tc2.error_message = str(e)

    suite.add_test(tc2)

    # 测试3: JSON 提取（带 markdown 代码块）
    tc3 = TestCase("json_extraction", "从 markdown 代码块提取 JSON")
    try:
        mock_llm = MockLLM({
            "精简": "```json\n" + json.dumps({
                "simplified_script_text": "提取成功",
                "simplification_summary": "测试"
            }) + "\n```"
        })

        simplifier = ScriptSimplifier()
        result = simplifier.process(mock_llm, script_text="测试")

        if result.simplified_script_text == "提取成功":
            tc3.passed = True
        else:
            tc3.error_message = "JSON 提取失败"

    except Exception as e:
        tc3.error_message = str(e)

    suite.add_test(tc3)

    return suite


# ============================================================================
# 测试: ConsistencyChecker
# ============================================================================

def test_consistency_checker():
    """测试一致性检查器"""
    suite = TestSuite("ConsistencyChecker 测试")

    # 测试1: 无问题
    tc1 = TestCase("no_issues", "未发现一致性问题")
    try:
        mock_llm = MockLLM({
            "一致性": json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "未发现问题"
            })
        })

        checker = ConsistencyChecker()
        result = checker.process(mock_llm, script_text="测试剧本")

        if not result.has_issues and len(result.issues) == 0:
            tc1.passed = True
        else:
            tc1.error_message = "应该没有问题"

    except Exception as e:
        tc1.error_message = str(e)

    suite.add_test(tc1)

    # 测试2: 发现问题
    tc2 = TestCase("has_issues", "发现角色混淆问题")
    try:
        mock_llm = MockLLM({
            "一致性": json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["小王子", "男孩"],
                        "description": "角色称呼不一致",
                        "suggestion": "统一使用'小王子'",
                        "affected_lines": {"start_line": 10, "end_line": 15},
                        "evidence": ["第10行称'男孩'"]
                    }
                ],
                "summary": "发现1个问题"
            })
        })

        checker = ConsistencyChecker()
        result = checker.process(mock_llm, script_text="测试剧本")

        if result.has_issues and len(result.issues) == 1:
            issue = result.issues[0]
            if issue.character_candidates == ["小王子", "男孩"]:
                tc2.passed = True
            else:
                tc2.error_message = "问题解析错误"
        else:
            tc2.error_message = "应该发现1个问题"

    except Exception as e:
        tc2.error_message = str(e)

    suite.add_test(tc2)

    return suite


# ============================================================================
# 测试: ScriptDivider
# ============================================================================

def test_divider():
    """测试分镜器"""
    suite = TestSuite("ScriptDivider 测试")

    # 测试1: 正常分镜
    tc1 = TestCase("normal_division", "正常分镜流程")
    try:
        mock_llm = MockLLM({
            "分镜": json.dumps({
                "total_shots": 2,
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 10,
                        "shot_name": "开场",
                        "script_excerpt": "片段1",
                        "time_of_day": "黄昏"
                    },
                    {
                        "index": 2,
                        "start_line": 11,
                        "end_line": 20,
                        "shot_name": "对话",
                        "script_excerpt": "片段2",
                        "time_of_day": "夜晚"
                    }
                ],
                "notes": "分镜说明"
            })
        })

        divider = ScriptDivider()
        result = divider.process(mock_llm, script_text="测试剧本")

        if result.total_shots == 2 and len(result.shots) == 2:
            if result.shots[0].shot_name == "开场":
                tc1.passed = True
            else:
                tc1.error_message = "镜头名称不匹配"
        else:
            tc1.error_message = "镜头数量不匹配"

    except Exception as e:
        tc1.error_message = str(e)

    suite.add_test(tc1)

    # 测试2: 直接返回列表格式
    tc2 = TestCase("list_format", "处理直接返回列表的格式")
    try:
        mock_llm = MockLLM({
            "分镜": json.dumps([
                {
                    "index": 1,
                    "start_line": 1,
                    "end_line": 5,
                    "shot_name": "镜头1",
                    "script_excerpt": "内容1"
                }
            ])
        })

        divider = ScriptDivider()
        result = divider.process(mock_llm, script_text="测试")

        if len(result.shots) == 1:
            tc2.passed = True
        else:
            tc2.error_message = "列表格式解析失败"

    except Exception as e:
        tc2.error_message = str(e)

    suite.add_test(tc2)

    # 测试3: 字段兼容性（title 代替 shot_name）
    tc3 = TestCase("field_compatibility", "兼容 title 字段")
    try:
        mock_llm = MockLLM({
            "分镜": json.dumps({
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 5,
                        "title": "使用title字段",  # 旧字段名
                        "script_excerpt": "内容"
                    }
                ]
            })
        })

        divider = ScriptDivider()
        result = divider.process(mock_llm, script_text="测试")

        if result.shots[0].shot_name == "使用title字段":
            tc3.passed = True
        else:
            tc3.error_message = "title 字段映射失败"

    except Exception as e:
        tc3.error_message = str(e)

    suite.add_test(tc3)

    # 测试4: 自动补全 index
    tc4 = TestCase("auto_index", "自动补全缺失的 index")
    try:
        mock_llm = MockLLM({
            "分镜": json.dumps({
                "shots": [
                    {
                        "start_line": 1,
                        "end_line": 5,
                        "shot_name": "镜头1",
                        "script_excerpt": "内容1"
                        # 缺少 index
                    },
                    {
                        "start_line": 6,
                        "end_line": 10,
                        "shot_name": "镜头2",
                        "script_excerpt": "内容2"
                        # 缺少 index
                    }
                ]
            })
        })

        divider = ScriptDivider()
        result = divider.process(mock_llm, script_text="测试")

        if result.shots[0].index == 1 and result.shots[1].index == 2:
            tc4.passed = True
        else:
            tc4.error_message = "index 自动补全失败"

    except Exception as e:
        tc4.error_message = str(e)

    suite.add_test(tc4)

    return suite


# ============================================================================
# 集成测试
# ============================================================================

def test_full_pipeline():
    """测试完整处理流程"""
    suite = TestSuite("完整流程集成测试")

    tc = TestCase("full_pipeline", "精简 -> 一致性检查 -> 分镜")
    try:
        # 准备 Mock LLM
        mock_llm = MockLLM({
            "精简": json.dumps({
                "simplified_script_text": "精简后的剧本",
                "simplification_summary": "删除冗余"
            }),
            "一致性": json.dumps({
                "has_issues": False,
                "issues": []
            }),
            "分镜": json.dumps({
                "total_shots": 1,
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 10,
                        "shot_name": "完整镜头",
                        "script_excerpt": "精简后的剧本"
                    }
                ]
            })
        })

        # 1. 精简
        simplifier = ScriptSimplifier()
        simplified = simplifier.process(mock_llm, script_text="原始剧本...")

        # 2. 一致性检查
        checker = ConsistencyChecker()
        consistency = checker.process(mock_llm, script_text=simplified.simplified_script_text)

        # 3. 分镜
        divider = ScriptDivider()
        division = divider.process(mock_llm, script_text=simplified.simplified_script_text)

        # 验证
        if (simplified.simplified_script_text == "精简后的剧本" and
            not consistency.has_issues and
            division.total_shots == 1):
            tc.passed = True
        else:
            tc.error_message = "流程输出不符合预期"

        # 验证 LLM 调用次数
        if mock_llm.get_call_count() != 3:
            tc.error_message = f"LLM 调用次数错误: {mock_llm.get_call_count()}"
            tc.passed = False

    except Exception as e:
        tc.error_message = str(e)

    suite.add_test(tc)
    return suite


# ============================================================================
# 主测试入口
# ============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("剧本处理器独立测试")
    print("=" * 60)

    suites = [
        test_simplifier(),
        test_consistency_checker(),
        test_divider(),
        test_full_pipeline()
    ]

    total_passed = 0
    total_failed = 0

    for suite in suites:
        suite.print_results()
        results = suite.run()
        total_passed += results['passed']
        total_failed += results['failed']

    print("\n" + "=" * 60)
    print("总体测试结果")
    print("=" * 60)
    print(f"总计: {total_passed + total_failed}")
    print(f"通过: {total_passed}")
    print(f"失败: {total_failed}")
    print(f"成功率: {total_passed / (total_passed + total_failed) * 100:.1f}%")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
