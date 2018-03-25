import sys
import argparse
import logging

import inberlinwohnen.parser
import inberlinwohnen.scraper

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")

args = parser.parse_args()

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger()

for site in args.sites:
    logger.debug(site)
    sitem = getattr(sys.modules[__name__], site)
    if args.scrape:
        scraper = getattr(sitem, "scraper")
        html = scraper.scrape()
        print html
    else:
        with open('samples/{}.txt'.format(site), 'r') as f:
            html = f.read()

    parser = getattr(sitem, "parser")
    print parser.parse()
