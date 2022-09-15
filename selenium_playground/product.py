import re


class Name:
    def __init__(self, value):
        self.value = value


class CurrentPrice:
    def __init__(self, current_price):
        self.value = current_price

    def fmt(self):
        trimmed = self.__trim_comma()
        return trimmed.__to_int()

    def __trim_comma(self):
        return CurrentPrice(self.value.replace(",", ""))

    def __to_int(self):
        return CurrentPrice(int(self.value))


class Price:
    def __init__(self, current_price, asking_price):
        self.current_price = current_price
        self.asking_price = asking_price

    def should_buy(self):
        return self.current_price.value < self.asking_price


class Inventory:
    large_inventory = "在庫あり。"

    def __init__(self, value):
        self.value = value

    def fmt(self):
        if self.__is_few():
            return Inventory(100)

        trimmed = self.__trim_description()
        return trimmed.__to_int()

    def __is_few(self):
        return self.value == Inventory.large_inventory

    def __trim_description(self):
        return Inventory(re.sub("[^0-9]", "", self.value))

    def __to_int(self):
        return Inventory(int(self.value))

    def can_buy(self):
        return self.value > 0
