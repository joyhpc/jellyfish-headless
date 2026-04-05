"""
爆款题材测试 - 霸道总裁剧本处理
使用 Mock LLM 模拟完整流程
"""

import json
from script_processors_standalone import (
    ScriptSimplifier,
    ConsistencyChecker,
    ScriptOptimizer,
    ScriptDivider,
)


# 读取测试剧本
with open('/home/ubuntu/test_script_romance.txt', 'r', encoding='utf-8') as f:
    original_script = f.read()

print("=" * 80)
print("爆款题材测试：《意外的心动》- 霸道总裁爱上我")
print("=" * 80)
print(f"\n原始剧本长度: {len(original_script)} 字符")
print(f"原始剧本行数: {len(original_script.splitlines())} 行")


# ============================================================================
# Mock LLM 响应（模拟真实 LLM 的输出）
# ============================================================================

class TestLLM:
    """测试用 LLM，返回预设的高质量响应"""

    def __init__(self):
        self.call_count = 0

    def __call__(self, prompt: str) -> str:
        self.call_count += 1

        # 1. 精简剧本
        if "精简" in prompt:
            return json.dumps({
                "simplified_script_text": """《意外的心动》

第一幕：相遇
清晨，陆氏集团办公室。陆景琛（28岁，总裁）正批阅文件。新实习生林小暖（23岁）紧张进门，不慎将咖啡泼在陆景琛西装上。陆景琛冷冷让她出去，眼神闪过波动。

第二幕：误会
公司年会，林小暖醉酒走错房间，醒来发现在陆景琛床上，慌忙逃离。此后陆景琛频繁"刁难"她，林小暖战战兢兢。

第三幕：心动
出差途中，林小暖为保护文件被雨淋湿。陆景琛心疼地给她披上外套："以后不许这么傻。"两人心意相通。

第四幕：危机
陆景琛前未婚妻苏晴雪回国，设计陷害林小暖泄密。陆景琛被迫开除林小暖，心如刀割。

第五幕：真相
陆景琛查明真相，解除婚约，冲到林小暖公寓挽留："从今以后，我只要你。"

第六幕：结局
三个月后，两人举办盛大婚礼。陆景琛宣布："谁敢欺负她，就是和我作对。"
""",
                "simplification_summary": "删除了冗余的心理描写和环境描述，保留核心剧情线：相遇-误会-心动-危机-真相-结局。精简了人物外貌描写，保留关键动作和对话。"
            }, ensure_ascii=False)

        # 2. 一致性检查
        elif "一致性" in prompt:
            return json.dumps({
                "has_issues": False,
                "issues": [],
                "summary": "未发现角色混淆问题。主要角色陆景琛、林小暖、苏晴雪称呼一致，无代词指代混乱。"
            }, ensure_ascii=False)

        # 3. 智能分镜
        elif "分镜" in prompt:
            return json.dumps({
                "total_shots": 12,
                "shots": [
                    {
                        "index": 1,
                        "start_line": 1,
                        "end_line": 3,
                        "shot_name": "总裁办公室-陆景琛工作",
                        "script_excerpt": "清晨，陆氏集团办公室。陆景琛（28岁，总裁）正批阅文件。",
                        "time_of_day": "清晨"
                    },
                    {
                        "index": 2,
                        "start_line": 3,
                        "end_line": 4,
                        "shot_name": "林小暖进门-咖啡泼洒",
                        "script_excerpt": "新实习生林小暖（23岁）紧张进门，不慎将咖啡泼在陆景琛西装上。",
                        "time_of_day": "清晨"
                    },
                    {
                        "index": 3,
                        "start_line": 4,
                        "end_line": 5,
                        "shot_name": "陆景琛冷漠反应",
                        "script_excerpt": "陆景琛冷冷让她出去，眼神闪过波动。",
                        "time_of_day": "清晨"
                    },
                    {
                        "index": 4,
                        "start_line": 6,
                        "end_line": 7,
                        "shot_name": "年会-林小暖醉酒",
                        "script_excerpt": "公司年会，林小暖醉酒走错房间，醒来发现在陆景琛床上，慌忙逃离。",
                        "time_of_day": "夜晚"
                    },
                    {
                        "index": 5,
                        "start_line": 7,
                        "end_line": 8,
                        "shot_name": "陆景琛刁难林小暖",
                        "script_excerpt": "此后陆景琛频繁'刁难'她，林小暖战战兢兢。",
                        "time_of_day": "白天"
                    },
                    {
                        "index": 6,
                        "start_line": 9,
                        "end_line": 10,
                        "shot_name": "出差-雨中保护文件",
                        "script_excerpt": "出差途中，林小暖为保护文件被雨淋湿。",
                        "time_of_day": "傍晚"
                    },
                    {
                        "index": 7,
                        "start_line": 10,
                        "end_line": 11,
                        "shot_name": "陆景琛心疼-披外套",
                        "script_excerpt": "陆景琛心疼地给她披上外套：'以后不许这么傻。'两人心意相通。",
                        "time_of_day": "傍晚"
                    },
                    {
                        "index": 8,
                        "start_line": 12,
                        "end_line": 13,
                        "shot_name": "苏晴雪回国-设计陷害",
                        "script_excerpt": "陆景琛前未婚妻苏晴雪回国，设计陷害林小暖泄密。",
                        "time_of_day": "白天"
                    },
                    {
                        "index": 9,
                        "start_line": 13,
                        "end_line": 14,
                        "shot_name": "林小暖被开除",
                        "script_excerpt": "陆景琛被迫开除林小暖，心如刀割。",
                        "time_of_day": "白天"
                    },
                    {
                        "index": 10,
                        "start_line": 15,
                        "end_line": 16,
                        "shot_name": "陆景琛查明真相",
                        "script_excerpt": "陆景琛查明真相，解除婚约，冲到林小暖公寓挽留。",
                        "time_of_day": "夜晚"
                    },
                    {
                        "index": 11,
                        "start_line": 16,
                        "end_line": 17,
                        "shot_name": "公寓-深情告白",
                        "script_excerpt": "'从今以后，我只要你。'",
                        "time_of_day": "夜晚"
                    },
                    {
                        "index": 12,
                        "start_line": 18,
                        "end_line": 20,
                        "shot_name": "婚礼-霸气宣言",
                        "script_excerpt": "三个月后，两人举办盛大婚礼。陆景琛宣布：'谁敢欺负她，就是和我作对。'",
                        "time_of_day": "白天"
                    }
                ],
                "notes": "按照经典霸道总裁剧情结构分镜：相遇冲突-误会加深-心动瞬间-危机爆发-真相大白-圆满结局。共12个镜头，涵盖6幕剧情。"
            }, ensure_ascii=False)

        return "{}"


# ============================================================================
# 执行完整测试流程
# ============================================================================

test_llm = TestLLM()

print("\n" + "=" * 80)
print("步骤 1/4: 剧本精简")
print("=" * 80)

simplifier = ScriptSimplifier()
simplified = simplifier.process(test_llm, script_text=original_script)

print(f"\n✓ 精简完成")
print(f"  原文长度: {len(original_script)} 字符")
print(f"  精简后长度: {len(simplified.simplified_script_text)} 字符")
print(f"  压缩率: {(1 - len(simplified.simplified_script_text) / len(original_script)) * 100:.1f}%")
print(f"\n精简说明:")
print(f"  {simplified.simplification_summary}")

print(f"\n精简后剧本预览:")
print("-" * 80)
print(simplified.simplified_script_text[:300] + "...")
print("-" * 80)


print("\n" + "=" * 80)
print("步骤 2/4: 一致性检查")
print("=" * 80)

checker = ConsistencyChecker()
consistency = checker.process(test_llm, script_text=simplified.simplified_script_text)

print(f"\n✓ 检查完成")
print(f"  发现问题: {len(consistency.issues)} 个")
print(f"  检查结果: {'通过' if not consistency.has_issues else '需要修复'}")
if consistency.summary:
    print(f"  总结: {consistency.summary}")


print("\n" + "=" * 80)
print("步骤 3/4: 剧本优化")
print("=" * 80)

if consistency.has_issues:
    print("\n发现一致性问题，执行优化...")
    optimizer = ScriptOptimizer()
    optimized = optimizer.process(
        test_llm,
        script_text=simplified.simplified_script_text,
        consistency_json=json.dumps({
            "has_issues": consistency.has_issues,
            "issues": [
                {
                    "issue_type": issue.issue_type,
                    "character_candidates": issue.character_candidates,
                    "description": issue.description,
                    "suggestion": issue.suggestion
                }
                for issue in consistency.issues
            ]
        }, ensure_ascii=False)
    )
    final_script = optimized.optimized_script_text
    print(f"✓ 优化完成")
    print(f"  改动说明: {optimized.change_summary}")
else:
    final_script = simplified.simplified_script_text
    print("\n✓ 无需优化（未发现一致性问题）")


print("\n" + "=" * 80)
print("步骤 4/4: 智能分镜")
print("=" * 80)

divider = ScriptDivider()
division = divider.process(test_llm, script_text=final_script)

print(f"\n✓ 分镜完成")
print(f"  总镜头数: {division.total_shots}")
if division.notes:
    print(f"  分镜说明: {division.notes}")


print("\n" + "=" * 80)
print("分镜列表详情")
print("=" * 80)

for shot in division.shots:
    print(f"\n【镜头 {shot.index}】{shot.shot_name}")
    print(f"  时间: {shot.time_of_day or '未指定'}")
    print(f"  行号: {shot.start_line}-{shot.end_line}")
    print(f"  内容: {shot.script_excerpt[:60]}{'...' if len(shot.script_excerpt) > 60 else ''}")


print("\n" + "=" * 80)
print("测试统计")
print("=" * 80)
print(f"  LLM 调用次数: {test_llm.call_count}")
print(f"  原始剧本: {len(original_script)} 字符")
print(f"  精简后: {len(simplified.simplified_script_text)} 字符")
print(f"  压缩率: {(1 - len(simplified.simplified_script_text) / len(original_script)) * 100:.1f}%")
print(f"  一致性问题: {len(consistency.issues)} 个")
print(f"  分镜数量: {division.total_shots} 个")


print("\n" + "=" * 80)
print("分镜结构分析")
print("=" * 80)

# 按时间段统计
time_stats = {}
for shot in division.shots:
    time = shot.time_of_day or "未指定"
    time_stats[time] = time_stats.get(time, 0) + 1

print("\n时间段分布:")
for time, count in sorted(time_stats.items()):
    print(f"  {time}: {count} 个镜头")

# 剧情结构分析
print("\n剧情结构:")
structure = [
    ("相遇", [1, 2, 3]),
    ("误会", [4, 5]),
    ("心动", [6, 7]),
    ("危机", [8, 9]),
    ("真相", [10, 11]),
    ("结局", [12])
]

for act_name, shot_indices in structure:
    print(f"  {act_name}: 镜头 {', '.join(map(str, shot_indices))}")


print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
print("\n✓ 所有步骤执行成功")
print("✓ 剧本处理流程验证通过")
print("✓ 输出格式符合预期")
