from src.models import Base


async def init_db(engine):
    """
    Asynchronously create all tables defined in the metadata.

    Args:
        engine: An instance of an asynchronous SQLAlchemy engine.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
