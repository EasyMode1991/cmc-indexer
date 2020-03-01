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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    box = soup.select('ul[class*="cmc-details-panel-links"]') 
    t = box[0].find_all("span")
    titles = [x.attrs["title"] for x in t if "title" in x.attrs] 
    return titles

def extract_box_links(url): 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    box = soup.select('ul[class*="cmc-details-panel-links"]') 
    links = [l["href"] for l in box[0].find_all("a", href=True)]
    # return list(map(lambda x: x['href'], links))
    print(links)
    return links 

class CoinIndexer(object):

    def __init__(self, all_coins = False, new_coins = False):

        check = [all_coins, new_coins]
        true_count = len(list(filter(lambda x: x == True, check)))
        assert true_count == 0 or true_count == 1

        self.base_url = "https://coinmarketcap.com"
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
        all_currencies = list(map(lambda x: x.split("/")[2], all_currencies))
        all_currencies =  list(set(all_currencies))
        return list(map(lambda x: "http://coinmarketcap.com/currencies/" + x, all_currencies))

class CryptoCoin(object):

    def __init__(self, url):    
        print(url)
        assert "coinmarketcap.com/currencies/" in url
        self.url = url

    def _name(self):
        return re.sub("http://coinmarketcap.com/currencies/", "", self.url)

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
            titles = extract_box_titles(self.url)
            links = extract_box_links(self.url)
            print(titles, links)
            return dict(zip(extract_box_titles(self.url)[1:], extract_box_links(self.url)))
        except Exception as e:
            return {"error":f"failed to scrape links - {e}"}

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
