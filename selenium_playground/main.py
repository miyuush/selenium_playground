import chromedriver_binary # nopa
from selenium import webdriver

# Chrome のオプションを設定する
options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# Selenium Server に接続する
driver = webdriver.Remote(
    command_executor='http://chrome:4444/wd/hub',
    desired_capabilities=options.to_capabilities(),
    options=options,
)

# driver.implicitly_wait(5)

# driver.get("https://www.time-j.net/worldtime/country/jp")

# print(driver.("/html/body/div/div[6]/div[1]/div/p[5]").text)
# driver.quit()

# Selenium 経由でブラウザを操作する
driver.get('https://qiita.com')
print(driver.current_url)

# ブラウザを終了する
# driver.quit()
