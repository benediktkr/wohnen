import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    apartments = []

    apartment_list = soup.find('ul', {'class': 'remember-list'})
    if apartment_list:
        for apartment_item in apartment_list.find_all('li', {'class': 'tb-merkflat ipg'}):
            apartment_data = {}

            # extract price from title
            title = apartment_item.find('h3').text.strip()
            kaltmiete_str = title.split('|')[0].split(', ')[2]
            apartment_data['kaltmiete'] = float(kaltmiete_str.split()[0].replace(',', '.'))

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
