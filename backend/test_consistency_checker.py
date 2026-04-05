"""
一致性检查器完整验证测试
包含多种场景和边界情况
"""

import json
from consistency_checker_standalone import ConsistencyChecker, check_consistency


# ============================================================================
# 测试用例定义
# ============================================================================

TEST_CASES = [
    {
        "name": "案例1: 完美剧本（无问题）",
        "script": """陆景琛是陆氏集团的总裁，28岁，冷峻俊朗。
林小暖是新来的实习生，23岁，清纯可爱。
陆景琛对林小暖说："你好，欢迎加入公司。"
林小暖紧张地回答："陆总好，我会努力工作的。"
陆景琛点点头，继续批阅文件。""",
        "expected_issues": 0,
        "mock_response": {
            "has_issues": False,
            "issues": [],
            "summary": "未发现角色混淆问题。主要角色陆景琛、林小暖称呼一致，无代词指代混乱。"
        }
    },
    {
        "name": "案例2: 称呼不一致",
        "script": """第1幕: 小王子住在B612星球。
第2幕: 男孩遇到了飞行员。
第3幕: 金发少年说："请给我画一只羊。"
第4幕: 那个孩子笑了。""",
        "expected_issues": 1,
        "mock_response": {
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["小王子", "男孩", "金发少年", "孩子"],
                    "description": "同一角色在不同幕中使用了四种不同称呼（小王子、男孩、金发少年、孩子），可能让读者误以为是不同角色",
                    "suggestion": "统一使用'小王子'作为主要称呼，或在首次出现时明确说明'小王子（一个金发少年）'",
                    "affected_lines": {"start_line": 1, "end_line": 4},
                    "evidence": [
                        "第1幕: 小王子住在B612星球",
                        "第2幕: 男孩遇到了飞行员",
                        "第3幕: 金发少年说",
                        "第4幕: 那个孩子笑了"
                    ]
                }
            ],
            "summary": "发现1个角色混淆问题，建议统一角色称呼"
        }
    },
    {
        "name": "案例3: 代词指代混乱",
        "script": """陆景琛和林小暖在办公室。
他走过去拿起文件。
她看着他。
他说："这是你的。"
她接过文件。""",
        "expected_issues": 1,
        "mock_response": {
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["陆景琛", "林小暖"],
                    "description": "第2行'他'指代不明确，虽然根据性别可以推断是陆景琛，但在快速阅读时容易产生混淆",
                    "suggestion": "将'他走过去'改为'陆景琛走过去'，明确行为主体",
                    "affected_lines": {"start_line": 2, "end_line": 2},
                    "evidence": ["他走过去拿起文件"]
                }
            ],
            "summary": "发现1个代词指代混乱问题"
        }
    },
    {
        "name": "案例4: 行为归属错位",
        "script": """第1幕: 林小暖不小心将咖啡泼在了陆景琛的西装上。
第2幕: 陆景琛冷冷地说："出去。"
第3幕: 陆景琛为泼咖啡的事向林小暖道歉。""",
        "expected_issues": 1,
        "mock_response": {
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["陆景琛", "林小暖"],
                    "description": "第1幕中是林小暖泼了咖啡，但第3幕中却是陆景琛道歉，行为主体错位",
                    "suggestion": "第3幕应改为'林小暖为泼咖啡的事向陆景琛道歉'，或者如果确实是陆景琛道歉，需要补充说明原因（如陆景琛为自己的冷漠态度道歉）",
                    "affected_lines": {"start_line": 1, "end_line": 3},
                    "evidence": [
                        "第1幕: 林小暖不小心将咖啡泼在了陆景琛的西装上",
                        "第3幕: 陆景琛为泼咖啡的事向林小暖道歉"
                    ]
                }
            ],
            "summary": "发现1个行为归属错位问题"
        }
    },
    {
        "name": "案例5: 同名不同人",
        "script": """第1幕: 小李是公司的前台，负责接待访客。
第2幕: 小李是技术部的工程师，正在修复服务器。
第3幕: 小李在会议室主持董事会。""",
        "expected_issues": 1,
        "mock_response": {
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["小李（前台）", "小李（工程师）", "小李（董事）"],
                    "description": "三个不同的'小李'在不同场景中担任不同职位（前台、工程师、董事），但没有明确区分，容易让读者混淆",
                    "suggestion": "为不同的小李添加区分标识，如'前台小李'、'工程师小李'、'董事长小李'，或使用全名区分",
                    "affected_lines": {"start_line": 1, "end_line": 3},
                    "evidence": [
                        "第1幕: 小李是公司的前台",
                        "第2幕: 小李是技术部的工程师",
                        "第3幕: 小李在会议室主持董事会"
                    ]
                }
            ],
            "summary": "发现1个同名不同人问题"
        }
    },
    {
        "name": "案例6: 多个问题并存",
        "script": """第1幕: 小王子住在B612星球。
第2幕: 男孩和飞行员在沙漠中。他说："我来自很远的地方。"
第3幕: 金发少年遇到了狐狸。
第4幕: 他们成为了朋友。""",
        "expected_issues": 2,
        "mock_response": {
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["小王子", "男孩", "金发少年"],
                    "description": "同一角色使用了三种不同称呼",
                    "suggestion": "统一使用'小王子'",
                    "affected_lines": {"start_line": 1, "end_line": 3}
                },
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["男孩", "飞行员"],
                    "description": "第2幕中'他'指代不明确，可能是男孩或飞行员",
                    "suggestion": "明确指出是谁在说话",
                    "affected_lines": {"start_line": 2, "end_line": 2}
                }
            ],
            "summary": "发现2个角色混淆问题"
        }
    },
    {
        "name": "案例7: 边界情况 - 空剧本",
        "script": "",
        "expected_issues": 0,
        "mock_response": {
            "has_issues": False,
            "issues": [],
            "summary": "剧本为空，无法检查"
        }
    },
    {
        "name": "案例8: 边界情况 - 单角色剧本",
        "script": """陆景琛独自坐在办公室里。
陆景琛看着窗外。
陆景琛叹了口气。""",
        "expected_issues": 0,
        "mock_response": {
            "has_issues": False,
            "issues": [],
            "summary": "单角色剧本，称呼一致，无混淆问题"
        }
    }
]


# ============================================================================
# Mock LLM
# ============================================================================

class MockLLM:
    """模拟 LLM，根据测试用例返回预设响应"""

    def __init__(self, test_cases):
        self.test_cases = test_cases
        self.current_case_index = 0

    def __call__(self, prompt: str) -> str:
        """根据当前测试用例返回响应"""
        if self.current_case_index < len(self.test_cases):
            case = self.test_cases[self.current_case_index]
            response = case["mock_response"]
            return json.dumps(response, ensure_ascii=False)
        return json.dumps({"has_issues": False, "issues": [], "summary": "默认响应"}, ensure_ascii=False)

    def next_case(self):
        """切换到下一个测试用例"""
        self.current_case_index += 1


# ============================================================================
# 测试执行
# ============================================================================

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("一致性检查器完整验证测试")
    print("=" * 80)

    checker = ConsistencyChecker()
    mock_llm = MockLLM(TEST_CASES)

    passed = 0
    failed = 0

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n{'=' * 80}")
        print(f"测试 {i}/{len(TEST_CASES)}: {case['name']}")
        print("=" * 80)

        # 显示测试剧本
        print(f"\n【测试剧本】")
        print("-" * 80)
        if case['script']:
            print(case['script'][:200] + ("..." if len(case['script']) > 200 else ""))
        else:
            print("(空剧本)")
        print("-" * 80)

        # 执行检查
        try:
            result = checker.check(case['script'], mock_llm)

            # 验证结果
            print(f"\n【检查结果】")
            print(f"  发现问题: {result.has_issues}")
            print(f"  问题数量: {len(result.issues)}")
            print(f"  预期问题数: {case['expected_issues']}")

            # 详细输出
            if result.issues:
                print(f"\n【问题详情】")
                for j, issue in enumerate(result.issues, 1):
                    print(f"\n  问题 {j}:")
                    print(f"    类型: {issue.issue_type}")
                    print(f"    涉及角色: {', '.join(issue.character_candidates)}")
                    print(f"    描述: {issue.description[:100]}...")
                    print(f"    建议: {issue.suggestion[:100]}...")
                    if issue.affected_lines:
                        print(f"    影响行号: {issue.affected_lines}")
                    if issue.evidence:
                        print(f"    证据数量: {len(issue.evidence)}")

            if result.summary:
                print(f"\n【总结】")
                print(f"  {result.summary}")

            # 验证
            if len(result.issues) == case['expected_issues']:
                print(f"\n✅ 测试通过")
                passed += 1
            else:
                print(f"\n❌ 测试失败: 预期 {case['expected_issues']} 个问题，实际 {len(result.issues)} 个")
                failed += 1

        except Exception as e:
            print(f"\n❌ 测试异常: {str(e)}")
            failed += 1

        mock_llm.next_case()

    # 测试总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"  总测试数: {len(TEST_CASES)}")
    print(f"  通过: {passed} ✅")
    print(f"  失败: {failed} ❌")
    print(f"  通过率: {passed / len(TEST_CASES) * 100:.1f}%")

    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")


# ============================================================================
# 功能演示
# ============================================================================

def demo_usage():
    """功能演示"""
    print("\n" + "=" * 80)
    print("功能演示：实际使用场景")
    print("=" * 80)

    # 创建一个真实场景的 Mock LLM
    def demo_llm(prompt: str) -> str:
        return json.dumps({
            "has_issues": True,
            "issues": [
                {
                    "issue_type": "character_confusion",
                    "character_candidates": ["陆景琛", "陆总", "景琛"],
                    "description": "同一角色在不同场景使用了三种称呼，虽然读者可以理解，但在视频制作时可能造成混淆",
                    "suggestion": "建议在正式场合使用'陆景琛'或'陆总'，私密场合使用'景琛'，并在首次出现时明确说明",
                    "affected_lines": {"start_line": 1, "end_line": 10},
                    "evidence": [
                        "秘书称呼：陆总",
                        "林小暖称呼：陆景琛",
                        "亲密时刻：景琛"
                    ]
                }
            ],
            "summary": "发现1个称呼不一致问题，建议根据场景区分使用"
        }, ensure_ascii=False)

    script = """秘书敲门："陆总，新来的实习生到了。"
林小暖紧张地说："陆景琛先生，您好。"
陆景琛点点头。
晚上，林小暖轻声说："景琛，你还在工作吗？"
"""

    print("\n【演示剧本】")
    print(script)

    # 使用便捷函数
    result = check_consistency(script, demo_llm)

    print("\n【检查结果】")
    print(f"发现问题: {result['has_issues']}")
    print(f"问题数量: {len(result['issues'])}")

    if result['issues']:
        issue = result['issues'][0]
        print(f"\n问题类型: {issue['issue_type']}")
        print(f"涉及角色: {', '.join(issue['character_candidates'])}")
        print(f"问题描述: {issue['description']}")
        print(f"修改建议: {issue['suggestion']}")

    print(f"\n总结: {result['summary']}")


# ============================================================================
# 性能测试
# ============================================================================

def performance_test():
    """性能测试"""
    import time

    print("\n" + "=" * 80)
    print("性能测试")
    print("=" * 80)

    # 生成大型剧本
    large_script = "\n".join([
        f"第{i}幕: 角色{i % 5}在场景{i % 3}中进行动作{i % 10}。"
        for i in range(1, 101)
    ])

    print(f"\n测试剧本大小: {len(large_script)} 字符")
    print(f"测试剧本行数: {len(large_script.splitlines())} 行")

    def fast_mock_llm(prompt: str) -> str:
        return json.dumps({
            "has_issues": False,
            "issues": [],
            "summary": "性能测试"
        }, ensure_ascii=False)

    checker = ConsistencyChecker()

    # 预热
    checker.check(large_script, fast_mock_llm)

    # 正式测试
    iterations = 10
    start_time = time.time()

    for _ in range(iterations):
        checker.check(large_script, fast_mock_llm)

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations

    print(f"\n测试次数: {iterations}")
    print(f"总耗时: {end_time - start_time:.3f} 秒")
    print(f"平均耗时: {avg_time:.3f} 秒/次")
    print(f"吞吐量: {1 / avg_time:.1f} 次/秒")


# ============================================================================
# 主函数
# ============================================================================

if __name__ == "__main__":
    # 运行完整测试
    run_tests()

    # 功能演示
    demo_usage()

    # 性能测试
    performance_test()

    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)
