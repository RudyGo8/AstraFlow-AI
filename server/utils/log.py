
import os
import sys
import time

from loguru import logger

# 鏃ュ織瀛樺偍鐩綍
log_path = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_path):
    os.makedirs(log_path)  # 濡傛灉鐩綍涓嶅瓨鍦紝鍒欏垱寤?

# 鎸夊ぉ鍒涘缓鏃ュ織鐩綍
daily_log_path = os.path.join(log_path, time.strftime("%Y-%m-%d"))
if not os.path.exists(daily_log_path):
    os.makedirs(daily_log_path)

# 瀹氫箟鎸夌骇鍒垎寮鐨勬棩蹇楁枃浠惰矾寰?
log_path_debug = os.path.join(daily_log_path, 'debug.log')
log_path_info = os.path.join(daily_log_path, 'info.log')
log_path_error = os.path.join(daily_log_path, 'error.log')
log_path_warning = os.path.join(daily_log_path, 'warning.log')
log_path_sql = os.path.join(daily_log_path, 'sql.log')  # SQL 鏌ヨ鏃ュ織鏂囦欢

# 瀹氫箟鍚堝苟鍚庣殑鏃ュ織鏂囦欢璺緞
log_path_all = os.path.join(daily_log_path, 'all.log')

# 绉婚櫎榛樿鐨勬棩蹇楀鐞嗗櫒
logger.remove()

# 娣诲姞鎺у埗鍙版棩蹇楀鐞嗗櫒锛堝僵鑹茶緭鍑猴級
logger.add(
    sink=sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",  # 鎺у埗鍙拌緭鍑烘墍鏈夌骇鍒殑鏃ュ織
    colorize=True,  # 鍚敤褰╄壊杈撳嚭
    enqueue=True,  # 寮傛鍐欏叆鏃ュ織
)

# 娣诲姞鎸夌骇鍒垎寮鐨勬棩蹇楁枃浠跺鐞嗗櫒
logger.add(
    sink=log_path_debug,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 鍙褰?DEBUG 绾у埆鐨勬棩蹇?
    rotation="50 MB",  # 鏃ュ織鏂囦欢澶у皬杈惧埌 50MB 鏃惰疆鎹?
    retention="30 days",  # 鏃ュ織鏂囦欢淇濈暀 30 澶?
    compression="zip",  # 鍘嬬缉鏃ф棩蹇楁枃浠?
    encoding="utf-8",
    enqueue=True,  # 寮傛鍐欏叆鏃ュ織
    filter=lambda record: record["level"].name == "DEBUG",  # 鍙鐞?DEBUG 绾у埆鐨勬棩蹇?
)

logger.add(
    sink=log_path_info,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="INFO",  # 鍙褰?INFO 绾у埆鐨勬棩蹇?
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "INFO",  # 鍙鐞?INFO 绾у埆鐨勬棩蹇?
)

logger.add(
    sink=log_path_warning,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="WARNING",  # 鍙褰?WARNING 绾у埆鐨勬棩蹇?
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "WARNING",  # 鍙鐞?WARNING 绾у埆鐨勬棩蹇?
)

logger.add(
    sink=log_path_error,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="ERROR",  # 鍙褰?ERROR 绾у埆鐨勬棩蹇?
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["level"].name == "ERROR",  # 鍙鐞?ERROR 绾у埆鐨勬棩蹇?
)

# 娣诲姞 SQL 鏌ヨ鏃ュ織鏂囦欢澶勭悊鍣?
logger.add(
    sink=log_path_sql,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 璁板綍鎵鏈?SQL 鏌ヨ鏃ュ織
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: "sqlalchemy.engine" in record["name"],  # 鍙鐞?SQL 鏌ヨ鏃ュ織
)

# 娣诲姞鍚堝苟鍚庣殑鏃ュ織鏂囦欢澶勭悊鍣?
logger.add(
    sink=log_path_all,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",  # 璁板綍鎵鏈夌骇鍒殑鏃ュ織
    rotation="50 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
)

# 鑷畾涔夋棩蹇楅鑹?
logger.level("DEBUG", color="<blue>")  # DEBUG 绾у埆涓鸿摑鑹?
logger.level("INFO", color="<green>")  # INFO 绾у埆涓虹豢鑹?
logger.level("WARNING", color="<yellow>")  # WARNING 绾у埆涓洪噾鑹?
logger.level("ERROR", color="<red>")  # ERROR 绾у埆涓虹孩鑹?
