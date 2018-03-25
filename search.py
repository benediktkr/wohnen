import sys
import argparse
import logging

import inberlinwohnen.parser
import inberlinwohnen.scraper

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")

args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

for site in args.sites:
    logger.debug(site)
    sitem = getattr(sys.modules[__name__], site)
    if args.scrape:
        scraper = getattr(sitem, "scraper")
        html = scraper.scrape()
    else:
        with open('{}/sample.txt'.format(site), 'r') as f:
            html = f.read()

    parser = getattr(sitem, "parser")
    parser.parse()
