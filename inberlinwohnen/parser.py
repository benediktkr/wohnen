import logging

from bs4 import BeautifulSoup

from apartment import Apartment

logger = logging.getLogger(__name__)


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    apartments = []

    apartment_list = soup.find('ul', {'class': 'remember-list'})
    if apartment_list:
        for apartment_item in apartment_list.find_all('li', {'class': 'tb-merkflat ipg'}):
            # init with question mark
            apartment_data: Apartment = {'addr': '?', 'floor': '?', 'price': '?', 'rooms': '?', 'sqm': '?',
                                         'timeframe': '?', 'wbs': '?', 'year': '?', 'link': '?', 'image': '?'}

            # extract price from title
            title = apartment_item.find('h3').text.strip()
            kaltmiete_str = title.split('|')[0].split(', ')[2]
            apartment_data['price'] = float(kaltmiete_str.split()[0].replace(',', '.'))

            details_link = apartment_item.find('a', {'class': 'org-but'})
            if details_link:
                apartment_data['link'] = 'https://inberlinwohnen.de' + details_link['href']

            image_container = apartment_item.find('figure', {'class': 'flat-image wide'})
            if image_container:
                image_link = image_container['style'].split("(")[1].split(")")[0]
                apartment_data['image'] = image_link

            details_tables = apartment_item.findAll('table', {'class': 'tb-small-data'})
            for details_table in details_tables:
                for row in details_table.find_all('tr'):
                    label = row.find('th').text.strip()
                    value = row.find('td').text.strip()

                    if label == 'Zimmeranzahl:':
                        apartment_data['rooms'] = float(value.replace(',', '.'))
                    elif label == 'Wohnfläche:':
                        apartment_data['sqm'] = float(value.replace(',', '.').split()[0])
                    elif label == 'Kaltmiete:':
                        apartment_data['price'] = float(value.replace(',', '.').split()[0])
                    elif label == 'Adresse:':
                        apartment_data['addr'] = value
                    elif label == 'Etage:':
                        apartment_data['floor'] = value
                    elif label == 'Bezugsfertig ab:':
                        apartment_data['timeframe'] = value
                    elif label == 'Baujahr:':
                        apartment_data['year'] = value
                    elif label == 'WBS:':
                        apartment_data['wbs'] = value

            apartments.append(apartment_data)

    return apartments
