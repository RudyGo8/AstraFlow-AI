import os
import sys
import time

from loguru import logger

# 日志根目录
log_path = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_path):
    os.makedirs(log_path)  # 目录不存在时自动创建

# 按日期创建子目录
daily_log_path = os.path.join(log_path, time.strftime("%Y-%m-%d"))
if not os.path.exists(daily_log_path):
    os.makedirs(daily_log_path)

# 各级别日志文件
log_path_debug = os.path.join(daily_log_path, "debug.log")
log_path_info = os.path.join(daily_log_path, "info.log")
log_path_error = os.path.join(daily_log_path, "error.log")
log_path_warning = os.path.join(daily_log_path, "warning.log")
log_path_sql = os.path.join(daily_log_path, "sql.log")  # SQL 查询日志

# 汇总日志文件
log_path_all = os.path.join(daily_log_path, "all.log")

# 移除默认处理器
logger.remove()

# 控制台输出：彩色文本，方便开发排查
logger.add(
    sink=sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",  # 控制台输出所有级别日志
    colorize=True,  # 启用颜色
    enqueue=True,  # 异步写入
)

# 按级别写入独立文件
logger.add(
    sink=log_path_debug,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 仅记录 DEBUG
    rotation="50 MB",  # 单文件超过 50MB 自动轮转
    retention="30 days",  # 保留 30 天
    compression="zip",  # 历史日志压缩
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "DEBUG",  # 仅写入 DEBUG
)

logger.add(
    sink=log_path_info,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="INFO",  # 仅记录 INFO
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "INFO",  # 仅写入 INFO
)

logger.add(
    sink=log_path_warning,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="WARNING",  # 仅记录 WARNING
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "WARNING",  # 仅写入 WARNING
)

logger.add(
    sink=log_path_error,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="ERROR",  # 仅记录 ERROR
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "ERROR",  # 仅写入 ERROR
)

# 单独记录 SQL 日志，避免与业务日志混杂
logger.add(
    sink=log_path_sql,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 记录 SQLAlchemy 产生的调试日志
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: "sqlalchemy.engine" in record["name"],  # 仅写入 SQL 日志
)

# 汇总文件记录所有日志
logger.add(
    sink=log_path_all,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 记录所有级别日志
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
)

# 自定义控制台颜色
logger.level("DEBUG", color="<blue>")  # DEBUG 使用蓝色
logger.level("INFO", color="<green>")  # INFO 使用绿色
logger.level("WARNING", color="<yellow>")  # WARNING 使用黄色
logger.level("ERROR", color="<red>")  # ERROR 使用红色
