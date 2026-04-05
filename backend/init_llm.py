#!/usr/bin/env python3
"""
初始化默认LLM配置到数据库
"""

import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session_maker
from app.models.llm import Provider, Model, ModelCategoryKey


async def init_default_llm():
    """初始化默认的OpenAI配置"""
    async with async_session_maker() as db:
        # 检查是否已有provider
        from sqlalchemy import select
        result = await db.execute(select(Provider))
        existing = result.scalars().first()

        if existing:
            print("已存在LLM配置，跳过初始化")
            return

        # 创建默认provider（需要手动指定ID）
        provider_id = str(uuid.uuid4())[:8]
        provider = Provider(
            id=provider_id,
            name="OpenAI",
            base_url="https://api.openai.com/v1",
            api_key="sk-placeholder",  # 需要用户替换
        )
        db.add(provider)
        await db.flush()

        # 创建默认text模型
        model_id = str(uuid.uuid4())[:8]
        model = Model(
            id=model_id,
            provider_id=provider.id,
            name="gpt-4o-mini",
            category=ModelCategoryKey.text,
            is_default=True,
            params={"temperature": 0},
        )
        db.add(model)

        await db.commit()
        print("✓ 已创建默认LLM配置")
        print(f"  Provider ID: {provider_id}")
        print(f"  Provider: OpenAI")
        print(f"  Model ID: {model_id}")
        print(f"  Model: gpt-4o-mini")
        print("\n请配置正确的 API Key:")
        print(f"  方式1: 在 .env 中添加 OPENAI_API_KEY=your-key")
        print(f"  方式2: 直接修改数据库中 providers 表的 api_key 字段")


if __name__ == "__main__":
    asyncio.run(init_default_llm())
