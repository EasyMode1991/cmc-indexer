import requests
from bs4 import BeautifulSoup
import re
import json

def extract_links(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    return list(map(lambda x: x['href'], links))

def extract_box_titles(url):
    assert "http://www.coinmarketcap.com/currencies" in url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    box = soup.find('ul', class_ = 'list-unstyled details-panel-item--links')
    titles = box.find_all('li')
    return list(map(lambda x: x.find('span')['title'], titles))

def extract_box_links(url):
    assert "http://www.coinmarketcap.com/currencies" in url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    box = soup.find('ul', class_ = 'list-unstyled details-panel-item--links')
    links = box.find_all('a', href = True)
    return list(map(lambda x: x['href'], links))


class CoinIndexer(object):

    def __init__(self, all_coins = False, new_coins = False):

        check = [all_coins, new_coins]
        true_count = len(list(filter(lambda x: x == True, check)))
        assert true_count == 0 or true_count == 1

        self.base_url = "http://www.coinmarketcap.com"
        self.index = {}

        if all_coins:
            self.url = self.base_url + "/all/views/all/"
        elif new_coins:
            self.url = self.base_url + "/new/"
        else:
            self.url = self.base_url

    def currency_pages(self):
        all_links = extract_links(self.url)
        all_currencies = list(filter(lambda x: 'currencies' in x, all_links))
        all_currencies = list(map(lambda x: x[:x.find("#") + 1], all_currencies))
        all_currencies = list(map(lambda x: x[:x.find("historical-data")], all_currencies))
        all_currencies =  list(set(all_currencies))
        all_currencies = list(filter(lambda x: x != "", all_currencies))
        return list(map(lambda x: "http://www.coinmarketcap.com" + x, all_currencies))

class CryptoCoin(object):

    def __init__(self, url):
        assert "coinmarketcap.com/currencies/" in url
        self.url = url

    def _name(self):
        return re.sub("http://www.coinmarketcap.com/currencies/", "", self.url[:-1])

    def ticker(self):
        response = requests.get('https://widgets.coinmarketcap.com/v1/ticker/{}/'.format(self._name()))
        return json.loads(response.text)

    def _twitter(self):
        links = extract_links(self.url)
        try:
            return list(filter(lambda x: 'twitter' in x and 'CoinMarketCap' not in x, links))[0]
        except:
            return None

    def _box_links(self):
        try:
            return dict(zip(extract_box_titles(self.url)[1:], extract_box_links(self.url)))
        except:
            return {}

    def summarise(self):
        links = self._box_links()
        info = {"Name":self._name(),
                "twitter":self._twitter()}
        result = {**info, **links}
        return result


def main():

    print("This is a module, use run.py")

if __name__ == "__main__":
    main()
