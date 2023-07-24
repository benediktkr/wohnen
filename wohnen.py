import argparse
import asyncio
import json
import logging
import sys
import time

import schedule

import config
from telegram_notifications import bot

import inberlinwohnen.parser
import inberlinwohnen.scraper

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")
parser.add_argument("--telegram", action="store_true", help="send to telegram")
parser.add_argument("--interval", type=int, default=0, help="run continuously with this interval in min")

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
        # html will be a list
        return f.read()


def main():
    for site in args.sites:
        logger.info("Checking {}".format(site))
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
            known_apartments = json.load(infile)

        new_apartments = [x for x in aparts if x not in known_apartments]

        with open(config.jsonfile, 'w') as outfile:
            json.dump(aparts, outfile)

        logger.info("Found {} new apartments".format(len(new_apartments)))

        if args.telegram:
            for apart in new_apartments:
                asyncio.run(bot.send_apartment(apart))
                time.sleep(2)


if __name__ == "__main__":
    if args.interval > 0:
        lower = round(args.interval - args.interval / 2)
        upper = round(args.interval + args.interval / 2)
        logger.info("Running every {} to {} minutes".format(lower, upper))
        schedule.every(lower).to(upper).minutes.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
