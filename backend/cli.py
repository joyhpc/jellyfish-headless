#!/usr/bin/env python3
"""
Jellyfish CLI - 无界面命令行工具
用于在无界面Ubuntu环境下使用Jellyfish的核心功能
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import click
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker
from app.chains.agents import (
    ScriptDividerAgent,
    ElementExtractorAgent,
    EntityMergerAgent,
    VariantAnalyzerAgent,
    ConsistencyCheckerAgent,
    ScriptOptimizerAgent,
    ScriptSimplifierAgent,
)
from app.dependencies import get_llm, get_nothinking_llm


@click.group()
def cli():
    """Jellyfish CLI - AI短剧生产工具命令行界面"""
    pass


@cli.command()
@click.argument('script_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（JSON格式）')
def simplify(script_file: str, output: Optional[str]):
    """精简剧本文本"""
    script_text = Path(script_file).read_text(encoding='utf-8')

    click.echo(f"正在精简剧本: {script_file}")
    click.echo(f"原始长度: {len(script_text)} 字符")

    async def run():
        async with async_session_maker() as db:
            llm = await get_nothinking_llm(db)
            agent = ScriptSimplifierAgent(llm)
            result = agent.extract(script_text=script_text)
            return result

    result = asyncio.run(run())

    click.echo(f"精简后长度: {len(result.simplified_script)} 字符")
    click.echo(f"精简说明: {result.notes or '无'}")

    if output:
        Path(output).write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
        click.echo(f"结果已保存到: {output}")
    else:
        click.echo("\n精简后的剧本:")
        click.echo(result.simplified_script)


@cli.command()
@click.argument('script_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（JSON格式）')
def optimize(script_file: str, output: Optional[str]):
    """优化剧本文本"""
    script_text = Path(script_file).read_text(encoding='utf-8')

    click.echo(f"正在优化剧本: {script_file}")

    async def run():
        async with async_session_maker() as db:
            llm = await get_llm(db)
            agent = ScriptOptimizerAgent(llm)
            result = agent.extract(script_text=script_text)
            return result

    result = asyncio.run(run())

    click.echo(f"优化完成")
    click.echo(f"优化说明: {result.notes or '无'}")

    if output:
        Path(output).write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
        click.echo(f"结果已保存到: {output}")
    else:
        click.echo("\n优化后的剧本:")
        click.echo(result.optimized_script)


@cli.command()
@click.argument('script_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（JSON格式）')
def check_consistency(script_file: str, output: Optional[str]):
    """检查剧本一致性（角色混淆）"""
    script_text = Path(script_file).read_text(encoding='utf-8')

    click.echo(f"正在检查剧本一致性: {script_file}")

    async def run():
        async with async_session_maker() as db:
            llm = await get_llm(db)
            agent = ConsistencyCheckerAgent(llm)
            result = agent.extract(script_text=script_text)
            return result

    result = asyncio.run(run())

    if result.has_issues:
        click.echo(f"发现 {len(result.issues)} 个一致性问题:")
        for i, issue in enumerate(result.issues, 1):
            click.echo(f"\n问题 {i}:")
            click.echo(f"  描述: {issue.description}")
            click.echo(f"  影响行: {issue.affected_lines}")
            click.echo(f"  建议: {issue.suggestion}")
    else:
        click.echo("未发现一致性问题")

    if output:
        Path(output).write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
        click.echo(f"\n结果已保存到: {output}")


@cli.command()
@click.argument('script_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（JSON格式）')
@click.option('--chapter-id', help='章节ID（如需写入数据库）')
@click.option('--write-db', is_flag=True, help='是否写入数据库')
def divide(script_file: str, output: Optional[str], chapter_id: Optional[str], write_db: bool):
    """将剧本分割为多个镜头"""
    script_text = Path(script_file).read_text(encoding='utf-8')

    click.echo(f"正在分镜: {script_file}")

    async def run():
        async with async_session_maker() as db:
            llm = await get_nothinking_llm(db)
            agent = ScriptDividerAgent(llm)
            result = agent.divide_script(script_text=script_text)

            if write_db:
                if not chapter_id:
                    click.echo("错误: 写入数据库需要提供 --chapter-id", err=True)
                    sys.exit(1)

                from app.services.studio.script_division import write_division_result_to_chapter
                await write_division_result_to_chapter(db, chapter_id=chapter_id, result=result)
                click.echo(f"已写入数据库，章节ID: {chapter_id}")

            return result

    result = asyncio.run(run())

    click.echo(f"分镜完成，共 {result.total_shots} 个镜头")

    if output:
        Path(output).write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
        click.echo(f"结果已保存到: {output}")
    else:
        click.echo("\n分镜列表:")
        for shot in result.shots:
            click.echo(f"  镜头 {shot.index}: {shot.shot_name} (行 {shot.start_line}-{shot.end_line})")


@cli.command()
@click.argument('extractions_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（JSON格式）')
@click.option('--historical', type=click.Path(exists=True), help='历史实体库JSON文件')
@click.option('--division', type=click.Path(exists=True), help='分镜结果JSON文件')
def merge_entities(extractions_file: str, output: Optional[str], historical: Optional[str], division: Optional[str]):
    """合并多镜头的实体信息"""
    extractions = json.loads(Path(extractions_file).read_text(encoding='utf-8'))

    historical_lib = {}
    if historical:
        historical_lib = json.loads(Path(historical).read_text(encoding='utf-8'))

    division_data = {}
    if division:
        division_data = json.loads(Path(division).read_text(encoding='utf-8'))

    click.echo(f"正在合并实体: {len(extractions)} 个镜头提取结果")

    async def run():
        async with async_session_maker() as db:
            llm = await get_llm(db)
            agent = EntityMergerAgent(llm)
            result = agent.extract(
                all_extractions_json=json.dumps(extractions, ensure_ascii=False),
                historical_library_json=json.dumps(historical_lib, ensure_ascii=False),
                script_division_json=json.dumps(division_data, ensure_ascii=False),
                previous_merge_json="{}",
                conflict_resolutions_json="[]",
            )
            return result

    result = asyncio.run(run())

    click.echo(f"合并完成")
    click.echo(f"角色数: {len(result.merged_library.get('characters', []))}")
    click.echo(f"场景数: {len(result.merged_library.get('scenes', []))}")
    click.echo(f"道具数: {len(result.merged_library.get('props', []))}")

    if result.conflicts:
        click.echo(f"发现 {len(result.conflicts)} 个冲突")

    if output:
        Path(output).write_text(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
        click.echo(f"结果已保存到: {output}")


@cli.command()
@click.argument('script_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), default='./output', help='输出目录')
def process_full(script_file: str, output_dir: str):
    """完整处理流程：精简 -> 优化 -> 一致性检查 -> 分镜"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    script_text = Path(script_file).read_text(encoding='utf-8')

    click.echo("=" * 60)
    click.echo("开始完整处理流程")
    click.echo("=" * 60)

    async def run():
        # 1. 精简
        click.echo("\n[1/4] 精简剧本...")
        async with async_session_maker() as db:
            llm_nothinking = await get_nothinking_llm(db)
            simplifier = ScriptSimplifierAgent(llm_nothinking)
            simplified = simplifier.extract(script_text=script_text)

            simplified_file = output_path / "01_simplified.json"
            simplified_file.write_text(json.dumps(simplified.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
            click.echo(f"   精简完成，保存到: {simplified_file}")

            # 2. 优化
            click.echo("\n[2/4] 优化剧本...")
            llm = await get_llm(db)
            optimizer = ScriptOptimizerAgent(llm)
            optimized = optimizer.extract(script_text=simplified.simplified_script)

            optimized_file = output_path / "02_optimized.json"
            optimized_file.write_text(json.dumps(optimized.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
            click.echo(f"   优化完成，保存到: {optimized_file}")

            # 3. 一致性检查
            click.echo("\n[3/4] 检查一致性...")
            checker = ConsistencyCheckerAgent(llm)
            consistency = checker.extract(script_text=optimized.optimized_script)

            consistency_file = output_path / "03_consistency.json"
            consistency_file.write_text(json.dumps(consistency.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')

            if consistency.has_issues:
                click.echo(f"   发现 {len(consistency.issues)} 个一致性问题，保存到: {consistency_file}")
            else:
                click.echo(f"   未发现一致性问题，保存到: {consistency_file}")

            # 4. 分镜
            click.echo("\n[4/4] 智能分镜...")
            divider = ScriptDividerAgent(llm_nothinking)
            division = divider.divide_script(script_text=optimized.optimized_script)

            division_file = output_path / "04_division.json"
            division_file.write_text(json.dumps(division.model_dump(), ensure_ascii=False, indent=2), encoding='utf-8')
            click.echo(f"   分镜完成，共 {division.total_shots} 个镜头，保存到: {division_file}")

            return {
                'simplified': simplified,
                'optimized': optimized,
                'consistency': consistency,
                'division': division
            }

    results = asyncio.run(run())

    click.echo("\n" + "=" * 60)
    click.echo("处理完成！")
    click.echo("=" * 60)
    click.echo(f"\n所有结果已保存到: {output_path}")
    click.echo(f"  - 精简剧本: 01_simplified.json")
    click.echo(f"  - 优化剧本: 02_optimized.json")
    click.echo(f"  - 一致性检查: 03_consistency.json")
    click.echo(f"  - 分镜结果: 04_division.json ({results['division'].total_shots} 个镜头)")


@cli.command()
def test_connection():
    """测试数据库和LLM连接"""
    click.echo("测试数据库连接...")

    async def test_db():
        try:
            async with async_session_maker() as session:
                from sqlalchemy import text
                result = await session.execute(text("SELECT 1"))
                click.echo("✓ 数据库连接成功")
                return True
        except Exception as e:
            click.echo(f"✗ 数据库连接失败: {e}", err=True)
            return False

    db_ok = asyncio.run(test_db())

    click.echo("\n测试LLM连接...")
    try:
        async def test_llm():
            async with async_session_maker() as db:
                llm = await get_llm(db)
                click.echo("✓ LLM配置加载成功")
                return True

        asyncio.run(test_llm())
    except Exception as e:
        click.echo(f"✗ LLM配置失败: {e}", err=True)
        click.echo("提示: 请在 .env 文件中配置 OPENAI_API_KEY 或其他LLM提供商")

    if db_ok:
        click.echo("\n✓ 基础环境检查通过")
    else:
        click.echo("\n✗ 环境检查失败", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
