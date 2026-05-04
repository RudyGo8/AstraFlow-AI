from models.sa_orm import SADeclarativeBase, _DB, close_orm, init_orm
from utils.log import logger


async def init_db():
    try:
        await init_orm()
        async with _DB.engine.begin() as conn:
            await conn.run_sync(SADeclarativeBase.metadata.create_all)
        logger.success("数据库连接初始化成功(SQLAlchemy)")
    except Exception as e:
        logger.error(f"数据库初始化失败: {type(e).__name__}: {e}", exc_info=True)
        raise


async def close_db():
    try:
        await close_orm()
        logger.success("数据库连接已关闭(SQLAlchemy)")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {type(e).__name__}: {e}", exc_info=True)
