#!/usr/bin/env python3
"""
测试脚本 - 验证 CLI 基础功能（不依赖真实 LLM）
"""

import asyncio
from pathlib import Path
from sqlalchemy import text
from app.core.db import async_session_maker


async def test_database():
    """测试数据库连接"""
    print("测试1: 数据库连接")
    try:
        async with async_session_maker() as session:
            result = await session.execute(text("SELECT 1"))
            print("  ✓ 数据库连接成功")
            return True
    except Exception as e:
        print(f"  ✗ 数据库连接失败: {e}")
        return False


async def test_models():
    """测试模型导入"""
    print("\n测试2: 模型导入")
    try:
        from app.models.llm import Provider, Model, ModelCategoryKey
        from app.models.studio import Project, Chapter, Shot
        print("  ✓ 模型导入成功")
        return True
    except Exception as e:
        print(f"  ✗ 模型导入失败: {e}")
        return False


async def test_agents():
    """测试 Agent 导入"""
    print("\n测试3: Agent 导入")
    try:
        from app.chains.agents import (
            ScriptDividerAgent,
            ScriptSimplifierAgent,
            ScriptOptimizerAgent,
            ConsistencyCheckerAgent,
        )
        print("  ✓ Agent 导入成功")
        return True
    except Exception as e:
        print(f"  ✗ Agent 导入失败: {e}")
        return False


async def test_file_operations():
    """测试文件操作"""
    print("\n测试4: 文件操作")
    try:
        test_file = Path("../test_script.txt")
        if test_file.exists():
            content = test_file.read_text(encoding='utf-8')
            print(f"  ✓ 测试剧本文件存在 ({len(content)} 字符)")
            return True
        else:
            print("  ✗ 测试剧本文件不存在")
            return False
    except Exception as e:
        print(f"  ✗ 文件操作失败: {e}")
        return False


async def test_llm_config():
    """测试 LLM 配置"""
    print("\n测试5: LLM 配置")
    try:
        from sqlalchemy import select
        from app.models.llm import Provider, Model

        async with async_session_maker() as db:
            # 检查 provider
            result = await db.execute(select(Provider))
            providers = result.scalars().all()

            if not providers:
                print("  ⚠ 未找到 LLM Provider 配置")
                print("    运行: uv run python init_llm.py")
                return False

            # 检查 model
            result = await db.execute(select(Model))
            models = result.scalars().all()

            if not models:
                print("  ⚠ 未找到 LLM Model 配置")
                return False

            print(f"  ✓ 找到 {len(providers)} 个 Provider, {len(models)} 个 Model")

            # 检查 API key
            for provider in providers:
                if provider.api_key == "sk-placeholder":
                    print(f"  ⚠ Provider '{provider.name}' 使用占位符 API Key")
                    print("    请配置真实的 API Key 以使用 LLM 功能")
                else:
                    print(f"  ✓ Provider '{provider.name}' 已配置 API Key")

            return True
    except Exception as e:
        print(f"  ✗ LLM 配置检查失败: {e}")
        return False


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("Jellyfish 无界面版本 - 环境测试")
    print("=" * 60)

    results = []

    results.append(await test_database())
    results.append(await test_models())
    results.append(await test_agents())
    results.append(await test_file_operations())
    results.append(await test_llm_config())

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n✓ 所有测试通过！环境配置正确。")
        print("\n下一步:")
        print("  1. 配置真实的 API Key (如果还未配置)")
        print("  2. 运行: uv run python cli.py test-connection")
        print("  3. 运行: uv run python cli.py divide ../test_script.txt -o test_output.json")
    else:
        print(f"\n✗ {total - passed} 个测试失败，请检查环境配置。")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
