from loguru import logger

def setup_logging():
    logger.add("app.log", serialize=True)