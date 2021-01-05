import source.scraper.adorama
import source.scraper.amazon
import source.scraper.bestbuy
import source.scraper.bhphotovideo
import source.scraper.canadacomputers
import source.scraper.costco
import source.scraper.ebgames
import source.scraper.microcenter
import source.scraper.newegg
import source.scraper.playstation
import source.scraper.samsclub
import source.scraper.toysrus
import source.scraper.walmart

from source.scraper.common import ScraperFactory


def init_scrapers(config, drivers):
    return [ScraperFactory.create(drivers, url) for url in config.urls]
