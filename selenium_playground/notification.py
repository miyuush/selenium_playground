import os

from slack_sdk.webhook import WebhookClient


class Notification:
    def __init__(self, name, price, inventory, url):
        self.name = name
        self.price = price
        self.inventory = inventory
        self.url = url
        self.client = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])

    def send_slack(self):
        text, blocks = self.__gen_send_content()
        res = self.client.send(text=text, blocks=blocks)
        print(res)

    def __gen_send_content(self):
        first_message = "定時報告"
        if self.price.should_buy():
            first_message = "<!channel> 買い時！:smile_cat:"

        text = f"{first_message}\n*<{self.url}|{self.name.value}>*\n \
                *価格* *在庫*\n{self.price.current_price.value} {self.inventory.value}"
        blocks = [
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
                    {"type": "plain_text", "text": "{} 円".format(self.price.current_price.value)},
                    {"type": "plain_text", "text": "{} 個".format(self.inventory.value)},
                ],
            },
            {"type": "divider"},
        ]
        return text, blocks
