import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ScrapingService:
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub",
            options=options,
        )

    def scrape(self):
        self.driver.get(self.url)

        price = self.__scrape_price()
        inventory = self.__scrape_inventory()
        cart_button = self.__scrape_cart_button()
        self.driver.quit()
        return Price(price), inventory, cart_button

    def __scrape_price(self):
        try:
            elem_core_price_div = self.driver.find_element(By.ID, "corePrice_feature_div")
            elem_price_whole = elem_core_price_div.find_element(By.CLASS_NAME, "a-price-whole")
        except NoSuchElementException:
            print("現在は売ってないよ")

        return elem_price_whole.text

    def __scrape_inventory(self):
        try:
            elem_availability = self.driver.find_element(By.ID, "availability")
            elem_size_medium = elem_availability.find_element(By.CLASS_NAME, "a-size-medium")
        except NoSuchElementException:
            print("在庫が無いよ")

        return elem_size_medium.text

    def __scrape_cart_button(self):
        try:
            elem_add_to_cart_button = self.driver.find_element(By.ID, "add-to-cart-button")
        except NoSuchElementException:
            print("在庫が無いよ")

        return elem_add_to_cart_button


class Product:
    def __init__(self, price, asking_price, inventory, can_buy):
        self.current_price = price
        self.asking_price = asking_price
        self.inventory = inventory
        self.can_buy = can_buy

    def print_product_info(self):
        print("価格：", self.current_price.value, "在庫：", self.inventory)

    def should_buy(self):
        return self.current_price.value < self.asking_price


class Price:
    def __init__(self, value):
        self.value = value

    def fmt(self):
        return self.__trim_comma().__to_int()

    def __trim_comma(self):
        return Price(self.value.replace(",", ""))

    def __to_int(self):
        return Price(int(self.value))


if __name__ == "__main__":
    with open("selenium_playground/config.json") as f:
        config = json.load(f)
        url = config["product1"]["url"]
        asking_price = config["product1"]["asking_price"]

    scraping_service = ScrapingService(url)
    price, inventory, cart_button = scraping_service.scrape()
    price_fmt = price.fmt()
    product = Product(price_fmt, asking_price, inventory, cart_button)
    product.print_product_info()
    print(product.should_buy())
