import requests
import time


s = requests.Session()

search_url = 'https://inberlinwohnen.de/wp-content/themes/ibw/skript/search-flats.php'
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
    'q': 'srch',
    'lang': 'de',
    'qtype': 'advanced',
    'order': 'mietpreis_nettokalt',
    'odx': 'ASC',
    'bez': '',
    'qmiete_min': '',
    'qmiete_max': '1000',
    'qqm_min': '50',
    'qqm_max': '',
    'qrooms_min': '2',
    'qrooms_max': '4',
    'qetage_min': '',
    'qetage_max': '',
    'qbaujahr_min': '',
    'qbaujahr_max': '',
    'qheizung_zentral': '0',
    'qheizung_etage': '0',
    'qenergy_fernwaerme': '0',
    'qheizung_nachtstrom': '0',
    'qheizung_ofen': '0',
    'qheizung_gas': '0',
    'qheizung_oel': '0',
    'qheizung_solar': '0',
    'qheizung_erdwaerme': '0',
    'qheizung_fussboden': '0',
    'qbalkon_loggia_terrasse': '0',  # was 1 in my capture. verified manually that this will return flats with and without balcony
    'qgarten': '0',
    'qwbs': 'must_not',
    'qbarrierefrei': '0',
    'qmoebliert': '0',
    'qgaeste_wc': '0',
    'qaufzug': '0',
    'qstellplatz': '0',
    'qkeller': '0',
    'qbadewanne': '0',
    'qdusche': '0',
}

def scrape():
    balcony_search = s.post(search_url, data=search_data, headers=search_headers)
    print "Balcony search http res: {}".format(balcony_search.status_code)

    # The web UI sleeps for a few seconds here, lets mimick that
    # It seemst to work without, but better to mimick more
    print "Sleeping for 5 seconds..."
    time.sleep(5.0)

    html_result = s.get(result_url, headers=result_headers)

    return html_result.text.encode("utf-8")
