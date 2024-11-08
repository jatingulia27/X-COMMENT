import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def load_cookies_from_file(driver, cookie_file_path):
    try:
        with open(cookie_file_path, 'r') as cookie_file:
            all_cookies = json.load(cookie_file)
            for cookies in all_cookies:
                for cookie in cookies:
                    driver.add_cookie(cookie)
                yield cookies  
                driver.delete_all_cookies()  
        logger.info(f"Cookies loaded from {cookie_file_path}")
    except FileNotFoundError:
        logger.error(f"Cookie file not found: {cookie_file_path}")
    except Exception as e:
        logger.error(f"Error loading cookies: {e}")

# Function to open a Twitter profile page and attempt to click the "Follow" button
def follow_account(driver, account_url):
    try:
        # Navigate to the Twitter account URL
        driver.get(account_url)
        logger.info(f"Navigated to account URL: {account_url}")

        # Wait for the follow button to be clickable and click it
        try:
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-testid, "follow")]'))
            )
            follow_button.click()
            logger.info("Successfully followed the account.")
        except Exception as e:
            logger.error("Error finding or clicking the Follow button: %s", e)
    except Exception as e:
        logger.error(f"An error occurred while trying to follow the account: {e}")


def main(cookie_file_path, account_url):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get('https://twitter.com/login')

        for cookies in load_cookies_from_file(driver, cookie_file_path):
            driver.refresh() 
            follow_account(driver, account_url)
            time.sleep(2)

    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")
    finally:
        driver.quit()  

# Example usage
cookie_file_path = 'cookies_list.json'  
account_url = 'https://x.com/GOP'  

main(cookie_file_path, account_url)
