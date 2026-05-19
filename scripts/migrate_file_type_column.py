import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import text
from ai_platform.config.resource import create_engine


async def migrate():
    engine = create_engine()
    async with engine.begin() as conn:
        await conn.execute(
            text("ALTER TABLE knowledge_base_file ALTER COLUMN file_type TYPE VARCHAR(100)")
        )
        print("表 knowledge_base_file 的 file_type 字段已更新为 VARCHAR(100)")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate())
