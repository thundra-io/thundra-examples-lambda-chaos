import json
import logging

logger = logging.getLogger(__name__)

cnf = {}

try:
    with open('config.json') as json_config:
        cnf = json.load(json_config)
except Exception as e:
    logging.error("couldn't load config.json file: %s", e)
