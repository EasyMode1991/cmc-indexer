import index
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import os

def write_coin_to_csv(d):
    if "results.csv" not in os.listdir("results"):
        with open("results/results.csv", "w") as f:
            fieldnames = [k for k in d]
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writerow(d)
    else:
        with open("results/results.csv", "a") as f:
            fieldnames = [k for k in d]
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writerow(d)

def main():

    parser = argparse.ArgumentParser(description = "Create an index of URLs from CoinMarketCap")
    count = parser.add_mutually_exclusive_group(required=True)
    count.add_argument('--all', action='store_true', help = 'indexes every coin (could take a while)')
    count.add_argument('--new', action= 'store_true', help = 'indexes the newest 100 coins')
    count.add_argument('--top', action = 'store_true' , help = 'indexes the top 100 coins')
    args = parser.parse_args()

    executor = ThreadPoolExecutor(max_workers = 10)

    if args.top:
        print("INDEXING TOP100 COINS")
        i = index.CoinIndexer()
        for e in i.currency_pages():
            print(e)
            c = index.CryptoCoin(e)
            executor.submit(write_coin_to_csv(c.summarise()))

    elif args.new:
        print("INDEXING NEW COINS")
        i = index.CoinIndexer(new_coins = True)
        for e in i.currency_pages():
            print(e)
            c = index.CryptoCoin(e)
            executor.submit(write_coin_to_csv(c.summarise()))

    elif args.all:
        i = index.CoinIndexer(all_coins = True)
        print("INDEXING ALL THE COINS")
        for e in i.currency_pages():
            print(e)
            c = index.CryptoCoin(e)
            executor.submit(write_coin_to_csv(c.summarise()))

if __name__ == "__main__":
    main()
