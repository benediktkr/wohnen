import argparse
import json
import logging
import sys

import inberlinwohnen.parser
import inberlinwohnen.scraper

import config

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")
parser.add_argument("--email", type=str, nargs="+", help="email addresses to send notify about new flats")

args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(config.loglevel)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_sample(site):
    logger.warning("Using sample file for {}".format(site))
    with open('{}/sample.txt'.format(site), 'r') as f:
        ## html will be a list
        return f.read()


if __name__ == "__main__":
    for site in args.sites:
        logger.debug(site)
        sitem = getattr(sys.modules[__name__], site)
        if args.scrape:
            scraper = getattr(sitem, "scraper")
            html = scraper.scrape(config.min_rooms, config.max_rooms, config.max_rent, config.wbs)
        else:
            scraper = None
            html = get_sample(site)

        parser = getattr(sitem, "parser")
        aparts = parser.parse(html)

        with open(config.jsonfile, 'r') as infile:
            known_aparts = json.load(infile)

        new_aparts = [x for x in aparts if x not in known_aparts]

        with open(config.jsonfile, 'w') as outfile:
            json.dump(aparts, outfile)
