from typing import Final


class CurrentPrice:
    """Deals with current product prices."""

    def __init__(self, value: int) -> None:
        """
        Args:
            value (int): Current product price.
        """
        self.value: int = value

    def is_cheap(self, asking_price: int) -> bool:
        """Determine if the current product price is lower than the asking price.

        Args:
            asking_price (int): Price to buy at this price.

        Returns:
            bool: If the price is lower than the asking price, True.
        """
        return self.value < asking_price


class CurrentInventory:
    """Deals with current product inventory."""

    NO_INVENTORY: Final[int] = 0

    def __init__(self, value: int) -> None:
        """
        Args:
            value (int): Current product inventory.
        """
        self.value: int = value

    def is_inventory(self) -> bool:
        """Determine if product is in stock.

        Returns:
            bool: True if in stock.
        """
        return self.value > self.NO_INVENTORY
