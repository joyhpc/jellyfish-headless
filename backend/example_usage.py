"""
实际使用示例 - 连接真实 LLM
"""

import os
from script_processors_standalone import (
    ScriptSimplifier,
    ConsistencyChecker,
    ScriptOptimizer,
    ScriptDivider,
)


# ============================================================================
# LLM 适配器
# ============================================================================

class OpenAIAdapter:
    """OpenAI API 适配器"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    def __call__(self, prompt: str) -> str:
        """调用 OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            return response.choices[0].message.content
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")


class AnthropicAdapter:
    """Anthropic Claude API 适配器"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.model = model

    def __call__(self, prompt: str) -> str:
        """调用 Anthropic API"""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)

            response = client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        except ImportError:
            raise ImportError("请安装 anthropic: pip install anthropic")


class OllamaAdapter:
    """Ollama 本地模型适配器"""

    def __init__(self, model: str = "qwen2.5:14b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def __call__(self, prompt: str) -> str:
        """调用 Ollama API"""
        try:
            import requests

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            return response.json()["response"]
        except ImportError:
            raise ImportError("请安装 requests: pip install requests")


# ============================================================================
# 完整处理流程
# ============================================================================

def process_script_full_pipeline(script_text: str, llm_adapter):
    """完整的剧本处理流程"""

    print("=" * 60)
    print("开始处理剧本")
    print("=" * 60)

    # 步骤1: 精简剧本
    print("\n[1/4] 精简剧本...")
    simplifier = ScriptSimplifier()
    simplified = simplifier.process(llm_adapter, script_text=script_text)
    print(f"✓ 精简完成")
    print(f"  原文长度: {len(script_text)} 字符")
    print(f"  精简后长度: {len(simplified.simplified_script_text)} 字符")
    print(f"  精简说明: {simplified.simplification_summary[:100]}...")

    # 步骤2: 一致性检查
    print("\n[2/4] 一致性检查...")
    checker = ConsistencyChecker()
    consistency = checker.process(llm_adapter, script_text=simplified.simplified_script_text)
    print(f"✓ 检查完成")
    print(f"  发现问题: {len(consistency.issues)} 个")

    # 步骤3: 优化修复（如果有问题）
    final_script = simplified.simplified_script_text
    if consistency.has_issues:
        print("\n[3/4] 优化修复...")
        import json
        optimizer = ScriptOptimizer()
        optimized = optimizer.process(
            llm_adapter,
            script_text=simplified.simplified_script_text,
            consistency_json=json.dumps({
                "has_issues": consistency.has_issues,
                "issues": [
                    {
                        "issue_type": issue.issue_type,
                        "character_candidates": issue.character_candidates,
                        "description": issue.description,
                        "suggestion": issue.suggestion,
                        "affected_lines": issue.affected_lines,
                        "evidence": issue.evidence
                    }
                    for issue in consistency.issues
                ]
            }, ensure_ascii=False)
        )
        final_script = optimized.optimized_script_text
        print(f"✓ 优化完成")
        print(f"  改动说明: {optimized.change_summary[:100]}...")
    else:
        print("\n[3/4] 跳过优化（无需修复）")

    # 步骤4: 智能分镜
    print("\n[4/4] 智能分镜...")
    divider = ScriptDivider()
    division = divider.process(llm_adapter, script_text=final_script)
    print(f"✓ 分镜完成")
    print(f"  总镜头数: {division.total_shots}")

    # 输出分镜列表
    print("\n" + "=" * 60)
    print("分镜列表")
    print("=" * 60)
    for shot in division.shots:
        print(f"\n镜头 {shot.index}: {shot.shot_name}")
        print(f"  行号: {shot.start_line}-{shot.end_line}")
        print(f"  时间: {shot.time_of_day or '未指定'}")
        print(f"  内容: {shot.script_excerpt[:80]}...")

    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)

    return {
        "simplified": simplified,
        "consistency": consistency,
        "division": division,
        "final_script": final_script
    }


# ============================================================================
# 使用示例
# ============================================================================

def example_with_openai():
    """使用 OpenAI 的示例"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置环境变量 OPENAI_API_KEY")
        return

    llm = OpenAIAdapter(api_key=api_key, model="gpt-4")

    script = """
    黄昏时分，撒哈拉沙漠。一架小型飞机的引擎突然熄火，飞机开始急速下坠。
    驾驶舱内，飞行员拼命拉动操纵杆，但无济于事。飞机重重地撞在沙丘上，
    扬起漫天黄沙。

    第二天清晨，飞行员从残骸中爬出来，浑身是伤。他环顾四周，只有无尽的沙漠。
    突然，他听到一个稚嫩的声音："请给我画一只羊。"

    飞行员转过身，看到一个金发的小男孩站在他面前。男孩穿着一件绿色的外套，
    围着一条金色的围巾。
    """

    process_script_full_pipeline(script, llm)


def example_with_anthropic():
    """使用 Anthropic Claude 的示例"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("请设置环境变量 ANTHROPIC_API_KEY")
        return

    llm = AnthropicAdapter(api_key=api_key)

    script = """
    黄昏时分，撒哈拉沙漠。一架小型飞机的引擎突然熄火，飞机开始急速下坠。
    驾驶舱内，飞行员拼命拉动操纵杆，但无济于事。飞机重重地撞在沙丘上，
    扬起漫天黄沙。

    第二天清晨，飞行员从残骸中爬出来，浑身是伤。他环顾四周，只有无尽的沙漠。
    突然，他听到一个稚嫩的声音："请给我画一只羊。"

    飞行员转过身，看到一个金发的小男孩站在他面前。男孩穿着一件绿色的外套，
    围着一条金色的围巾。
    """

    process_script_full_pipeline(script, llm)


def example_with_ollama():
    """使用 Ollama 本地模型的示例"""
    llm = OllamaAdapter(model="qwen2.5:14b")

    script = """
    黄昏时分，撒哈拉沙漠。一架小型飞机的引擎突然熄火，飞机开始急速下坠。
    驾驶舱内，飞行员拼命拉动操纵杆，但无济于事。飞机重重地撞在沙丘上，
    扬起漫天黄沙。

    第二天清晨，飞行员从残骸中爬出来，浑身是伤。他环顾四周，只有无尽的沙漠。
    突然，他听到一个稚嫩的声音："请给我画一只羊。"

    飞行员转过身，看到一个金发的小男孩站在他面前。男孩穿着一件绿色的外套，
    围着一条金色的围巾。
    """

    process_script_full_pipeline(script, llm)


def example_single_processor():
    """单独使用某个处理器的示例"""
    from test_processors import MockLLM
    import json

    # 使用 Mock LLM 进行演示
    mock_llm = MockLLM({
        "分镜": json.dumps({
            "total_shots": 3,
            "shots": [
                {
                    "index": 1,
                    "start_line": 1,
                    "end_line": 3,
                    "shot_name": "飞机坠毁",
                    "script_excerpt": "黄昏时分，撒哈拉沙漠。飞机坠落。",
                    "time_of_day": "黄昏"
                },
                {
                    "index": 2,
                    "start_line": 4,
                    "end_line": 5,
                    "shot_name": "飞行员醒来",
                    "script_excerpt": "第二天清晨，飞行员爬出残骸。",
                    "time_of_day": "清晨"
                },
                {
                    "index": 3,
                    "start_line": 6,
                    "end_line": 8,
                    "shot_name": "遇见小王子",
                    "script_excerpt": "小男孩出现，请求画羊。",
                    "time_of_day": "清晨"
                }
            ]
        })
    })

    # 只使用分镜器
    divider = ScriptDivider()
    result = divider.process(mock_llm, script_text="测试剧本")

    print("\n分镜结果:")
    for shot in result.shots:
        print(f"  {shot.index}. {shot.shot_name} ({shot.time_of_day})")


if __name__ == "__main__":
    print("剧本处理器使用示例")
    print("\n可用的示例:")
    print("1. example_with_openai() - 使用 OpenAI GPT-4")
    print("2. example_with_anthropic() - 使用 Anthropic Claude")
    print("3. example_with_ollama() - 使用 Ollama 本地模型")
    print("4. example_single_processor() - 单独使用某个处理器")
    print("\n运行示例:")

    # 运行单处理器示例（不需要真实 API）
    example_single_processor()
