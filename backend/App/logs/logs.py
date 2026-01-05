import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(filename)s:%(lineno)d - %(funcName)s()-%(levelname)s-%(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("logs.log",maxBytes=1_000_000,backupCount=5)
    ]
)

logger=logging.getLogger(__name__)
sql_logger=logging.getLogger("sqlalchemy.engine")
sql_handler= RotatingFileHandler("sql_logs.log",maxBytes=100_000,backupCount=2)
sql_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
sql_logger.addHandler(sql_handler)
sql_logger.setLevel(logging.INFO)
sql_logger.propagate=False