import logging
import logging.config
import json

with open('test_log.json', 'r') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.error("test")
