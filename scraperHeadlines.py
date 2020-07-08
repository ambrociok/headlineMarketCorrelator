import scraper
import time

def automation():
    y = scraper.Scraper()
    y.createCSV()

if __name__ == '__main__':
    automation()
    time.sleep(300)