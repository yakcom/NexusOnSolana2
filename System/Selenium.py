from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
from loguru import logger
import time,os

def Get(Url,Token):
    logger.trace(f'Open selenium for {Url}')
    Settings = Options()
    Settings.add_argument('--no-sandbox')
    Settings.add_argument("--headless=new")
    Settings.add_argument("--lang=en-US")
    Settings.add_argument("--hide-scrollbars")
    Settings.add_argument('--disable-dev-shm-usage')
    Settings.add_argument("--disable-crash-reporter")
    Settings.add_argument('--log-level=3')
    Settings.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36")
    Settings.add_argument("--ignore-certificate-errors")
    for a in range(3):
        try:
            Browser = webdriver.Chrome(Settings)
            Browser.set_window_size(1080, 1080)
            Browser.set_page_load_timeout(30)
            try:Browser.get(Url)
            except:pass
            time.sleep(7)
            Browser.save_screenshot(os.path.join('Previews',f'{Token["Address"]}.png'))
            Page = Browser.page_source
            Browser.quit()
            return Page
        except Exception as e:
            Browser.quit()
            raise ValueError(f'{Url} selenium error {e}"')