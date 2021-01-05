import argparse
import logging
import pathlib
import sys
import os

# get version
version = 'v0.0.1'
version_path = pathlib.Path(__file__).resolve().parent / 'version.txt'
if version_path.is_file():
    with open(version_path, 'r') as f:
        version = f.read().strip()


# logging must be configured before the next few imports
log_format = '{levelname:.1s}{asctime} [{name}] {message}'
log_level = logging.DEBUG , logging.INFO
logging.info(f'starting {version} with args: {" ".join(sys.argv)}')


from alerter import init_alerters
from source.config import parse_config
from driver import init_drivers
from source.scraper import init_scrapers
from hunter import hunt


def main():
    try:
        dirPath = os.path
        yamlConfig = 'C:/Users/ajayakumar/Desktop/Pet Projects/InformerCaptainBot/config/amazon_rtx_3070.yaml'
        #alerters = init_alerters(args)
        config = parse_config(yamlConfig)
        drivers = init_drivers()
        scrapers = init_scrapers(config, drivers)
        hunt(config, scrapers)
    except Exception as ex:
        logging.exception(ex)
        logging.exception('caught exception')
        sys.exit(1)


if __name__ == '__main__':
    main()
