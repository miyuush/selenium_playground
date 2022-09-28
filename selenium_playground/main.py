import json
import sys
import time

from jsonschema import ValidationError, validate
from notification import Notification
from product import CurrentInventory, CurrentPrice
from scraping_service import ScrapingService

INTERVAL = 3600


def is_correct_json(config_json, json_schema) -> bool:
    """Check the json structure with jsonschema.

    Args:
        config_json (dict): JSON data to be checked.
        json_schema (dict): Definition of jsonschema.

    Returns:
        bool: Whether config_json follows json_schema
    """
    try:
        validate(config_json, json_schema)
    except ValidationError as e:
        print(e.message)
        return False
    return True


if __name__ == "__main__":
    with open("selenium_playground/config/schema.json") as schema:
        json_schema = json.load(schema)

    with open("selenium_playground/config/config.json") as config:
        config_json = json.load(config)

    if not is_correct_json(config_json, json_schema):
        sys.exit()

    while True:
        for product in config_json["products"]:
            scraping_service: ScrapingService = ScrapingService(product)
            scraped_name, scraped_price, scraped_inventory = scraping_service.scrape()

            current_price: int = scraped_price.format_()
            current_inventory: int = scraped_inventory.format_()

            notify: Notification = Notification(
                scraped_name,
                CurrentPrice(current_price),
                CurrentInventory(current_inventory),
                product["url"],
                product["asking_price"],
            )
            notify.send_slack()

        time.sleep(INTERVAL)
