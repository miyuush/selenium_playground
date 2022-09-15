import json
import time

from notification import Notification
from product import Price
from scraping_service import ScrapingService

INTERVAL = 3600


if __name__ == "__main__":
    with open("selenium_playground/config.json") as f:
        config = json.load(f)

    while True:
        for product in config.values():
            scraping_service = ScrapingService(product)
            name, unformatted_price, unformatted_inventory = scraping_service.scrape()

            current_price = unformatted_price.fmt()
            price = Price(current_price, product["asking_price"])
            inventory = unformatted_inventory.fmt()

            notify = Notification(name, price, inventory, product["url"])
            notify.send_slack()

        time.sleep(INTERVAL)


# Todo
# docstringを書く
# タイプヒンティング、mypyあたりを調べる
# vscodeで保存時にpythonのフォーマッタを実行するように設定する
