# wohnen

There's nothing to be written about the housing sitation in Berlin that hasn't been said before.

This is a scraper and parser for inberlinwohnen.de, where the city of Berlin advertises it's flats. The program is built with a sort-of modular design so it can be extended to work for more sites.

## Usage

The config is a bit of a mess, it uses a mix of command line arguments and the file `config.py`.

```shell
» ./wohnen.py --help
usage: wohnen.py [-h] [--scrape] [--email EMAIL [EMAIL ...]] sites [sites ...]

positional arguments:
  sites                 list of sites to check

optional arguments:
  -h, --help            show this help message and exit
  --scrape              actually scrape
  --email EMAIL [EMAIL ...]
                        email addresses to send notify about new flats

```

Set the search parameters in config.py:

```python
min_rooms = 2
max_rooms = 3
max_rent = 700
# 0 = no wbs
# 1 = only wbs
# 2 = doesnt matter
wbs = 0
```
