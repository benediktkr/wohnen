import logging

import requests

logger = logging.getLogger(__name__)

s = requests.Session()

search_url = 'https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php'
result_url = 'https://inberlinwohnen.de/suchergebnis/'

search_headers = {
    'accept': '*/*',
    'origin': 'https://inberlinwohnen.de',
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

result_headers = {
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

common_headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'inberlinwohnen.de',
    'referer': 'https://inberlinwohnen.de/wohnungsfinder/'
}
s.headers.update(common_headers)

search_data = {
    'q': 'wf-save-srch',
    'save': 'false',
    'miete_min': '',
    'miete_max': '',
    'qm_min': '',
    'qm_max': '',
    'rooms_min': '',
    'rooms_max': '',
    'etage_min': '',
    'etage_max': '',
    'baujahr_min': '',
    'baujahr_max': '',
    'heizung_zentral': 'false',
    'heizung_etage': 'false',
    'energy_fernwaerme': 'false',
    'heizung_nachtstrom': 'false',
    'heizung_ofen': 'false',
    'heizung_gas': 'false',
    'heizung_oel': 'false',
    'heizung_solar': 'false',
    'heizung_erdwaerme': 'false',
    'heizung_fussboden': 'false',
    'seniorenwohnung': 'false',
    'maisonette': 'false',
    'etagen_dg': 'false',
    'balkon_loggia_terrasse': 'false',
    'garten': 'false',
    'wbs': 'all',
    'barrierefrei': 'false',
    'gaeste_wc': 'false',
    'aufzug': 'false',
    'stellplatz': 'false',
    'keller': 'false',
    'badewanne': 'false',
    'dusche': 'false',
}


def get_search(min_rooms, max_rooms, max_rent, wbs):
    wbs_map = {
        0: 'must_not',
        1: 'must',
        2: 'all',
    }
    s = search_data.copy()
    s['rooms_min'] = str(min_rooms)
    s['rooms_max'] = str(max_rooms)
    s['miete_max'] = str(max_rent)
    s['wbs'] = wbs_map[wbs]
    return s


def scrape(min_rooms, max_rooms, max_rent, wbs):
    search_d = get_search(min_rooms, max_rooms, max_rent, wbs)
    search = s.post(search_url, data=search_d, headers=search_headers)
    # search.raise_for_status()
    # parse result as json
    search_json = search.json()

    return search_json['searchresults']
