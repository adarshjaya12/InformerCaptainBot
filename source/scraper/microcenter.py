from scraper.common import ScrapeResult, Scraper, ScraperFactory


class MicroCenterScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        details = self.soup.body.find('div', id='details', class_='inline')
        if details:

            # get name of product
            tag = details.select_one('h1 span')
            if tag:
                alert_content += tag.text.strip() + '\n'
            else:
                self.logger.warning(f'missing title: {self.url}')

            # get listed price
            tag = details.find('div', id='options-pricing')
            price_str = self.set_price(tag)
            if price_str:
                alert_subject = f'In Stock for {price_str}'
            else:
                self.logger.warning(f'missing price: {self.url}')

            # check for add to cart button
            tag = details.select_one('aside#cart-options form')
            if tag and 'add to cart' in str(tag).lower():
                self.alert_subject = alert_subject
                self.alert_content = f'{alert_content.strip()}\n{self.url}'

            # check for in-store inventory
            tag = details.select_one('div#pnlInventory span.inventoryCnt')
            if tag and 'in stock' in str(tag).lower():
                self.alert_subject = alert_subject
                self.alert_content = f'{alert_content.strip()}\n{self.url}'

        else:
            self.logger.warning(f'missing details div: {self.url}')


@ScraperFactory.register
class MicroCenterScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'microcenter'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return MicroCenterScrapeResult
