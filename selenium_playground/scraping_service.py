from product import CurrentPrice, Inventory, Name
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ScrapingService:
    def __init__(self, product):
        self.url = product["url"]
        self.elem_name = product["elem_name"]
        self.elem_price = product["elem_price"]
        self.elem_inventory = product["elem_inventory"]
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub",
            options=options,
        )

    def scrape(self):
        self.driver.get(self.url)
        name = self.__scrape_name()
        unformatted_price = self.__scrape_price()
        unformatted_inventory = self.__scrape_inventory()
        self.driver.quit()
        return Name(name), CurrentPrice(unformatted_price), Inventory(unformatted_inventory)

    def __scrape_name(self):
        try:
            elem_productTitle = self.driver.find_element(By.ID, self.elem_name["id"])
        except NoSuchElementException:
            print("商品名が取得できないよ")

        return elem_productTitle.text

    def __scrape_price(self):
        try:
            elem_core_price_div = self.driver.find_element(By.ID, self.elem_price["id"])
            elem_price_whole = elem_core_price_div.find_element(
                By.CLASS_NAME, self.elem_price["class"]
            )
        except NoSuchElementException:
            print("現在は売ってないよ")

        return elem_price_whole.text

    def __scrape_inventory(self):
        try:
            elem_availability = self.driver.find_element(By.ID, self.elem_inventory["id"])
            elem_size_medium = elem_availability.find_element(
                By.CLASS_NAME, self.elem_inventory["class"]
            )
        except NoSuchElementException:
            return "0"

        return elem_size_medium.text
