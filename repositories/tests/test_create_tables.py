import pytest

from repositories import engine
from tables import BaseModel, Device, Code


@pytest.mark.asyncio
async def test_create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        for table in [Device, Code]:
            table = table.__tablename__
            await conn.run_sync(engine.dialect.has_table, table)
