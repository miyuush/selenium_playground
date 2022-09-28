import os
from typing import Final, Tuple

from product import CurrentInventory, CurrentPrice
from scraping_service import ScrapedName
from slack_sdk.webhook import WebhookClient


class Notification:
    """Handle the notification process to Slack."""

    def __init__(
        self,
        name: ScrapedName,
        price: CurrentPrice,
        inventory: CurrentInventory,
        url: str,
        asking_price: int,
    ) -> None:
        """
        Args:
            name (ScrapedName): Product Name.
            price (CurrentPrice): Current Product Price.
            inventory (CurrentInventory): Current Product Inventory.
            url (str): URL of the product page.
            asking_price (int): Price to buy at this price.
        """
        self.name: Final[ScrapedName] = name
        self.price: Final[CurrentPrice] = price
        self.inventory: Final[CurrentInventory] = inventory
        self.url: Final[str] = url
        self.asking_price: Final[int] = asking_price
        self.client = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])

    def send_slack(self) -> None:
        """Send Slack."""
        text, blocks = self.__gen_send_content()
        res = self.client.send(text=text, blocks=blocks)
        print(res)

    def __gen_send_content(self) -> Tuple[str, list]:
        """Generate the content of the message to be sent to Slack.

        Returns:
            Tuple[str, list]: Message Content.
        """
        first_message: str = "定時報告"

        should_buy: Final[bool] = (
            self.price.is_cheap(self.asking_price) and self.inventory.is_inventory()
        )
        if should_buy:
            first_message = "<!channel> 買い時！:smile_cat:"

        text: Final[
            str
        ] = f"{first_message}\n*<{self.url}|{self.name.value}>*\n \
                *価格* *在庫*\n{self.price.value} {self.inventory.value}"
        blocks: Final[list] = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": first_message},
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*<{}|{}>*".format(self.url, self.name.value)},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": ":moneybag: *価格* :moneybag: "},
                    {"type": "mrkdwn", "text": "*在庫*"},
                    {"type": "plain_text", "text": "{} 円".format(self.price.value)},
                    {"type": "plain_text", "text": "{} 個".format(self.inventory.value)},
                ],
            },
            {"type": "divider"},
        ]
        return text, blocks
