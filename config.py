from logging import DEBUG, INFO, WARNING, ERROR

jsonfile = "./wohnen.json"
loglevel = DEBUG

## Set searches
## This only has an effect when run with --scrape
min_rooms = 1
max_rooms = 2
max_rent = 600
# 0 = No wbs
# 1 = only wbs
# 2 = doesnt matter
wbs = 2

