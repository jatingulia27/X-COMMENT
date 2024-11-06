import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to load cookies from a specified file and add them to the browser session
def load_cookies_from_file(driver, cookie_file_path):
    try:
        with open(cookie_file_path, 'r') as cookie_file:
            cookies = json.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
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

# Main function to initialize the WebDriver, load cookies, and follow an account
def main(cookie_files, account_url):
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (optional for headless)
    chrome_options.add_argument("--no-sandbox")  # Avoid sandboxing in headless mode

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Loop through each set of cookies and attempt to follow the account
        for cookie_file in cookie_files:
            logger.info(f"Using cookies from: {cookie_file}")
            driver.get('https://twitter.com/login')  # Visit the login page first to set cookies
            load_cookies_from_file(driver, cookie_file)  # Load cookies
            driver.refresh()  # Refresh the page to apply cookies

            # Attempt to follow the account
            follow_account(driver, account_url)

            # Clear cookies for the next account
            driver.delete_all_cookies()
            logger.info("Cookies cleared for the next account.")
            time.sleep(2)

    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after the process

# Example usage:
cookie_files = [
    'twitter_cookies22.json',  # Replace with actual cookie file paths
    # Add more cookie file paths as needed
]
account_url = 'https://x.com/GOP'  # Replace with the actual account URL to follow

main(cookie_files, account_url)
