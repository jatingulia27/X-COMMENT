import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to load cookies from a specified file and add them to the browser session
def load_cookies_from_file(driver, cookie_file_path):
    try:
        with open(cookie_file_path, 'r') as cookie_file:
            cookies = json.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print(f"Cookies loaded from {cookie_file_path}")
    except FileNotFoundError:
        print(f"Cookie file not found: {cookie_file_path}")
    except Exception as e:
        print(f"Error loading cookies: {e}")

# Function to open a Twitter profile page and attempt to click the "Follow" button
def follow_account(driver, account_url):
    try:
        # Navigate to the Twitter account URL
        driver.get(account_url)
        print(f"Navigated to account URL: {account_url}")
        time.sleep(3)  # Wait for the page to load

        # Attempt to locate and click the "Follow" button
        try:
            follow_button = driver.find_element(By.XPATH, '//button[contains(@data-testid, "follow")]')
            follow_button.click()
            print("Successfully followed the account.")
        except Exception as e:
            print("Error finding or clicking the Follow button:", e)
    except Exception as e:
        print(f"An error occurred while trying to follow the account: {e}")

# Main function to initialize the WebDriver, load cookies, and follow an account
def main(cookie_files, account_url):
    driver = webdriver.Chrome()
    try:
        # Loop through each set of cookies and attempt to follow the account
        for cookie_file in cookie_files:
            print(f"\nUsing cookies from: {cookie_file}")
            driver.get('https://twitter.com/login')
            load_cookies_from_file(driver, cookie_file)  # Load cookies
            driver.refresh()  # Refresh the page to apply cookies
            time.sleep(2)

            # Attempt to follow the account
            follow_account(driver, account_url)

            # Clear cookies for the next account
            driver.delete_all_cookies()
            print("Cookies cleared for the next account.")
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred in the main function: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after the process

# Example usage:
cookie_files = [
    'twitter_cookies22.json', 
    # Add more cookie file paths as needed
]
account_url = 'https://x.com/elonmusk'  # Replace with the actual account URL to follow

main(cookie_files, account_url)
