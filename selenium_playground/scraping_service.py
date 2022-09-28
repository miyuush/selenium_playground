import re
from typing import Final, Tuple

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ScrapedName:
    """Deals with the name of the product that was scraped."""

    def __init__(self, value: str) -> None:
        """
        Args:
            value (str): Scraped product name.
        """
        self.value: str = value


class ScrapedPrice:
    """Deals with scraped product prices."""

    def __init__(self, value: str) -> None:
        """
        Args:
            value (str): Scraped product price.
        """
        self.value: str = value

    def format_(self) -> int:
        """Format the scraped product price from a string to a number.

        Returns:
            int: Product Price.
        """
        self.__trim_comma()
        return self.__to_int()

    def __trim_comma(self) -> None:
        """Remove commas from product prices."""
        self.value = self.value.replace(",", "")

    def __to_int(self) -> int:
        """Cast the product price from a string to a number.

        Returns:
            int: Product Price.
        """
        return int(self.value)


class ScrapedInventory:
    """Deals with scraped product inventory."""

    IN_STOCK: Final[str] = "在庫あり。"
    NO_STOCK: Final[str] = "一時的に在庫切れ; 入荷時期は未定です。"
    LARGE_INVENTORY: Final[int] = 100
    NO_INVENTORY: Final[int] = 0

    def __init__(self, value: str) -> None:
        """
        Args:
            value (str): Scraped product inventory.
        """
        self.value: str = value

    def format_(self) -> int:
        """Format the scraped product inventory from a string to a number.

        Returns:
            int: Product inventory.
        """
        if self.__is_many():
            return self.LARGE_INVENTORY

        if self.__is_none():
            return self.NO_INVENTORY

        self.__trim_description()
        return self.__to_int()

    def __is_many(self) -> bool:
        """Determine if inventory is high.

        If there is a large inventory, it will say,
        "在庫あり。" value is obtained in the scrape.

        Returns:
            bool: True if there is a large inventory.
        """
        return self.value == self.IN_STOCK

    def __is_none(self) -> bool:
        """Determine if there is no inventory.

        If there is no inventory, it will say,
        "一時的に在庫切れ; 入荷時期は未定です。"
        value is obtained in the scrape.

        Returns:
            bool: If there is no inventory, True.
        """
        return self.value == self.NO_STOCK

    def __trim_description(self) -> None:
        """Trim unnecessary descriptions other than inventory counts."""
        self.value = re.sub("[^0-9]", "", self.value)

    def __to_int(self) -> int:
        """Cast the product inventory from a string to a number.

        Returns:
            int: Product Inventory.
        """
        return int(self.value)


class ScrapingService:
    """Deals with scraping of web pages."""

    SOLD_OUT: Final[str] = "0"

    def __init__(self, product) -> None:
        """
        Args:
            product (dict): Information on the product page to be scraped.
        """
        self.url: Final[str] = product["url"]
        self.elem_name: Final[dict[str, str]] = product["elem_name"]
        self.elem_price: Final[dict[str, str]] = product["elem_price"]
        self.elem_inventory: Final[dict[str, str]] = product["elem_inventory"]
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub",
            options=options,
        )

    def scrape(self) -> Tuple[ScrapedName, ScrapedPrice, ScrapedInventory]:
        """Accessing and scraping web pages.

        Returns:
            Tuple[ScrapedName, ScrapedPrice, ScrapedInventory]:
                Scraped product name, product price, and product inventory.
        """
        self.driver.get(self.url)
        scraped_name: Final[str] = self.__scrape_name()
        scraped_price: Final[str] = self.__scrape_price()
        scraped_inventory: Final[str] = self.__scrape_inventory()
        self.driver.quit()
        return (
            ScrapedName(scraped_name),
            ScrapedPrice(scraped_price),
            ScrapedInventory(scraped_inventory),
        )

    def __scrape_name(self) -> str:
        """Scrape the product name element from the HTML source.

        Returns:
            str: Product Name.
        """
        try:
            elem_productTitle = self.driver.find_element(By.ID, self.elem_name["id"])
        except NoSuchElementException as e:
            return "商品名が取得できないよ: {}".format(e)

        return elem_productTitle.text

    def __scrape_price(self) -> str:
        """Scrape the product price element from the HTML source.

        Returns:
            str: Product Price.
        """
        try:
            elem_core_price_div = self.driver.find_element(By.ID, self.elem_price["id"])
            elem_price_whole = elem_core_price_div.find_element(
                By.CLASS_NAME, self.elem_price["class"]
            )
        except NoSuchElementException as e:
            print("現在は売ってないよ: ", e)
            return self.SOLD_OUT

        return elem_price_whole.text

    def __scrape_inventory(self) -> str:
        """Scrape the product inventory element from the HTML source.

        Returns:
            str: Product Inventory.
        """
        try:
            elem_availability = self.driver.find_element(By.ID, self.elem_inventory["id"])
            elem_size_medium = elem_availability.find_element(
                By.CLASS_NAME, self.elem_inventory["class"]
            )
        except NoSuchElementException as e:
            print("在庫が無いよ: ", e)
            return self.SOLD_OUT

        return elem_size_medium.text
