"""
一致性检查组件效果演示
展示各种角色混淆场景的检测能力
"""

import json
from consistency_checker_standalone import ConsistencyChecker


# ============================================================================
# 演示场景
# ============================================================================

DEMO_CASES = [
    {
        "title": "场景1: 完美剧本（无问题）",
        "script": """陆景琛是陆氏集团的总裁，冷峻而专业。
林小暖是新来的实习生，清纯而努力。
陆景琛对林小暖说："欢迎加入公司。"
林小暖紧张地回答："谢谢陆总，我会努力的。"
陆景琛点点头，继续工作。""",
        "expected": "无问题"
    },
    {
        "title": "场景2: 称呼不一致（常见问题）",
        "script": """第1幕：小王子住在B612星球上。
第2幕：男孩遇到了飞行员。
第3幕：金发少年说："请给我画一只羊。"
第4幕：那个孩子笑了起来。
第5幕：小王子继续他的旅程。""",
        "expected": "发现称呼不一致"
    },
    {
        "title": "场景3: 代词指代混乱",
        "script": """陆景琛和林小暖在办公室讨论项目。
他走到窗边，看着外面的风景。
她拿起文件，递给他。
他接过文件，仔细阅读。
她等待着他的回应。""",
        "expected": "发现代词指代混乱"
    },
    {
        "title": "场景4: 行为归属错位",
        "script": """第1幕：林小暖不小心打翻了咖啡，洒在陆景琛的西装上。
第2幕：陆景琛皱眉，冷冷地说："出去。"
第3幕：陆景琛为打翻咖啡的事向林小暖道歉。
第4幕：林小暖感动得流下眼泪。""",
        "expected": "发现行为归属错位"
    },
    {
        "title": "场景5: 同名不同人",
        "script": """第1幕：小李是公司前台，负责接待访客。
第2幕：小李是技术部经理，正在开会讨论项目。
第3幕：小李是财务总监，审批预算报告。
第4幕：三个小李在走廊相遇。""",
        "expected": "发现同名不同人"
    },
    {
        "title": "场景6: 复杂混淆（多个问题）",
        "script": """第1幕：小王子在星球上遇到了狐狸。
第2幕：男孩对它说："你愿意做我的朋友吗？"
第3幕：金发少年和狐狸成为了好朋友。
第4幕：他们一起看日落。
第5幕：孩子离开了星球，狐狸很伤心。""",
        "expected": "发现多个问题"
    }
]


# ============================================================================
# Mock LLM（模拟真实响应）
# ============================================================================

class DemoLLM:
    """演示用 LLM，返回高质量的检测结果"""

    def __call__(self, prompt: str) -> str:
        # 场景1: 完美剧本
        if "陆景琛是陆氏集团的总裁" in prompt:
            return json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "✅ 未发现角色混淆问题。角色称呼一致（陆景琛、林小暖），无代词指代混乱，行为归属清晰。"
            }, ensure_ascii=False)

        # 场景2: 称呼不一致
        elif "小王子住在B612星球" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["小王子", "男孩", "金发少年", "孩子"],
                        "description": "同一角色在5幕中使用了4种不同称呼（小王子、男孩、金发少年、孩子），容易让读者/观众产生混淆，误以为是不同角色。",
                        "suggestion": "建议统一使用'小王子'作为主要称呼。如需变化，可在首次出现时说明：'小王子（一个金发少年）'，后续保持一致。",
                        "affected_lines": {"start_line": 1, "end_line": 5},
                        "evidence": [
                            "第1幕: 小王子住在B612星球",
                            "第2幕: 男孩遇到了飞行员",
                            "第3幕: 金发少年说",
                            "第4幕: 那个孩子笑了",
                            "第5幕: 小王子继续"
                        ]
                    }
                ],
                "summary": "⚠️ 发现1个称呼不一致问题，建议统一角色称呼以提高可读性。"
            }, ensure_ascii=False)

        # 场景3: 代词指代混乱
        elif "陆景琛和林小暖在办公室讨论项目" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["陆景琛", "林小暖"],
                        "description": "第2行'他走到窗边'中的'他'指代不明确。虽然根据性别可以推断是陆景琛，但在快速阅读或视频制作时容易产生混淆。后续的'他'和'她'虽然性别明确，但首次出现的模糊指代会影响理解流畅度。",
                        "suggestion": "将'他走到窗边'改为'陆景琛走到窗边'，明确行为主体。后续可以使用代词，但首次行为应明确角色名。",
                        "affected_lines": {"start_line": 2, "end_line": 2},
                        "evidence": ["他走到窗边，看着外面的风景"]
                    }
                ],
                "summary": "⚠️ 发现1个代词指代混乱问题，建议首次行为明确角色名。"
            }, ensure_ascii=False)

        # 场景4: 行为归属错位
        elif "林小暖不小心打翻了咖啡" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["陆景琛", "林小暖"],
                        "description": "第1幕中是林小暖打翻了咖啡，但第3幕中却是陆景琛为打翻咖啡的事道歉，行为主体错位。这在逻辑上不合理，除非有特殊剧情设定（如陆景琛为自己的冷漠态度道歉）。",
                        "suggestion": "方案1：改为'林小暖为打翻咖啡的事向陆景琛道歉'，符合逻辑。方案2：如果确实是陆景琛道歉，需要补充说明原因，如'陆景琛为自己刚才的冷漠态度向林小暖道歉'。",
                        "affected_lines": {"start_line": 1, "end_line": 3},
                        "evidence": [
                            "第1幕: 林小暖不小心打翻了咖啡",
                            "第3幕: 陆景琛为打翻咖啡的事向林小暖道歉"
                        ]
                    }
                ],
                "summary": "⚠️ 发现1个行为归属错位问题，需要修正逻辑关系。"
            }, ensure_ascii=False)

        # 场景5: 同名不同人
        elif "小李是公司前台" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["小李（前台）", "小李（技术经理）", "小李（财务总监）"],
                        "description": "三个不同的'小李'在不同场景中担任不同职位（前台、技术经理、财务总监），但没有明确区分，容易让读者混淆。第4幕'三个小李在走廊相遇'证实了这是三个不同的人，但前三幕没有区分标识。",
                        "suggestion": "为不同的小李添加区分标识：'前台小李'、'技术部小李'、'财务部小李'，或使用全名区分（如'李明'、'李华'、'李强'）。",
                        "affected_lines": {"start_line": 1, "end_line": 4},
                        "evidence": [
                            "第1幕: 小李是公司前台",
                            "第2幕: 小李是技术部经理",
                            "第3幕: 小李是财务总监",
                            "第4幕: 三个小李在走廊相遇"
                        ]
                    }
                ],
                "summary": "⚠️ 发现1个同名不同人问题，需要添加区分标识。"
            }, ensure_ascii=False)

        # 场景6: 复杂混淆
        elif "小王子在星球上遇到了狐狸" in prompt:
            return json.dumps({
                "has_issues": True,
                "issues": [
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["小王子", "男孩", "金发少年", "孩子"],
                        "description": "同一角色使用了4种不同称呼（小王子、男孩、金发少年、孩子），称呼不一致。",
                        "suggestion": "统一使用'小王子'作为主要称呼。",
                        "affected_lines": {"start_line": 1, "end_line": 5},
                        "evidence": ["第1幕: 小王子", "第2幕: 男孩", "第3幕: 金发少年", "第5幕: 孩子"]
                    },
                    {
                        "issue_type": "character_confusion",
                        "character_candidates": ["男孩/小王子", "狐狸"],
                        "description": "第2幕中'它'指代狐狸，但'你'的主语不明确（应该是男孩/小王子）。第4幕'他们'指代不够清晰。",
                        "suggestion": "第2幕改为'小王子对狐狸说'，第4幕改为'小王子和狐狸一起看日落'。",
                        "affected_lines": {"start_line": 2, "end_line": 4}
                    }
                ],
                "summary": "⚠️ 发现2个角色混淆问题（称呼不一致 + 代词指代混乱）。"
            }, ensure_ascii=False)

        # 默认响应
        return json.dumps({
            "has_issues": False,
            "issues": [],
            "summary": "未发现明显的角色混淆问题。"
        }, ensure_ascii=False)


# ============================================================================
# 效果演示
# ============================================================================

def demo_consistency_checker():
    """演示一致性检查器的效果"""

    print("=" * 80)
    print("一致性检查组件效果演示")
    print("=" * 80)
    print()

    checker = ConsistencyChecker()
    demo_llm = DemoLLM()

    for i, case in enumerate(DEMO_CASES, 1):
        print(f"\n{'=' * 80}")
        print(f"演示 {i}/{len(DEMO_CASES)}: {case['title']}")
        print(f"预期结果: {case['expected']}")
        print("=" * 80)

        # 显示测试剧本
        print(f"\n【测试剧本】")
        print("-" * 80)
        print(case['script'])
        print("-" * 80)

        # 执行检查
        result = checker.check(case['script'], demo_llm)

        # 显示检查结果
        print(f"\n【检查结果】")
        print(f"  发现问题: {'是' if result.has_issues else '否'}")
        print(f"  问题数量: {len(result.issues)}")

        if result.summary:
            print(f"  总结: {result.summary}")

        # 显示问题详情
        if result.issues:
            print(f"\n【问题详情】")
            for j, issue in enumerate(result.issues, 1):
                print(f"\n  问题 {j}:")
                print(f"    类型: {issue.issue_type}")
                print(f"    涉及角色: {', '.join(issue.character_candidates)}")
                print(f"    描述: {issue.description}")
                print(f"    建议: {issue.suggestion}")

                if issue.affected_lines:
                    print(f"    影响行号: 第{issue.affected_lines['start_line']}-{issue.affected_lines['end_line']}行")

                if issue.evidence:
                    print(f"    证据:")
                    for evidence in issue.evidence[:3]:  # 只显示前3条
                        print(f"      - {evidence}")
                    if len(issue.evidence) > 3:
                        print(f"      ... 还有 {len(issue.evidence) - 3} 条证据")

        print()

    # 总结
    print("\n" + "=" * 80)
    print("演示总结")
    print("=" * 80)
    print()
    print("✅ 演示了6种典型场景:")
    print("   1. 完美剧本 - 无问题")
    print("   2. 称呼不一致 - 4种称呼")
    print("   3. 代词指代混乱 - '他'指代不明")
    print("   4. 行为归属错位 - 行为主体错误")
    print("   5. 同名不同人 - 3个'小李'")
    print("   6. 复杂混淆 - 多个问题并存")
    print()
    print("✅ 检测能力:")
    print("   - 准确识别各种角色混淆类型")
    print("   - 提供详细的问题描述")
    print("   - 给出具体的修改建议")
    print("   - 标注影响行号和证据")
    print()
    print("✅ 输出质量:")
    print("   - 结构化 JSON 格式")
    print("   - 可溯源（行号+证据）")
    print("   - 易于理解和处理")
    print()
    print("=" * 80)
    print("演示完成！")
    print("=" * 80)


if __name__ == "__main__":
    demo_consistency_checker()
