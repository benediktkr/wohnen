#coding: utf-8

import random
import time
from urlparse import urljoin
import logging

import requests

REDDIT = "https://www.reddit.com"
DEFAULTDOG = "https://i.redd.it/bqkh6gdv5so01.jpg"
logger = logging.getLogger(__name__)

dogreddits = [
    "PuppySmiles",
    "dogpictures"
]

def urls(result):
    return [a['data']['url'] for a in result['data']['children']]

def get_dogpics():
    session = requests.Session()
    session.headers.update({'User-Agent': 'This is /u/benediktkr fetching two dog pictures'})

    dogs = []
    for subreddit in dogreddits:
        d = session.get(urljoin(REDDIT, "/r/{}/.json".format(subreddit)))
        if d.status_code == 200:
            logger.debug("Got dogpics from /r/{}".format(subreddit))
            dogs.extend(urls(d.json()))

        logging.debug("Sleeping for 3 seconds between hitting reddit")
        time.sleep(3.0)

    return dogs

def get_random_dogpic():
    try:
        dogs = get_dogpics()
        return random.choice(dogs)
    except IndexError:
        # get_dogpics() returned an empty list
        return DEFAULTDOG
    except requests.exceptions.RequestException:
        return DEFAULTDOG

if __name__ == "__main__":
    print get_random_dogpic()
