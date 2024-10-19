from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

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
def comment_on_post(driver, post_url, comment_text):
    try:
        driver.get(post_url)
        print(f"Navigated to the post URL: {post_url}")
        time.sleep(5)

        comment_box = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
        comment_box.click()
        comment_box.send_keys(comment_text)
        print("Comment typed")

        tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
        tweet_button.click()
        print("Comment posted successfully!")

    except Exception as e:
        print(f"An error occurred while commenting: {e}")

# Main function to open the browser and set up cookies for multiple accounts
def main(cookie_files, post_url):
    driver = webdriver.Chrome()
    try:
        comment_text = "comment."
        for cookie_file in cookie_files:
            print(f"\nUsing cookies from: {cookie_file}")
            driver.get('https://twitter.com/login')
            time.sleep(2)

            load_cookies_from_file(driver, cookie_file)
            driver.refresh() 
            time.sleep(3)

            comment_on_post(driver, post_url, comment_text)

            # Clear cookies 
            driver.delete_all_cookies()
            print("Cookies cleared for the next account.")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")

    # Keep the browser open indefinitely
    print("The browser will remain open. Close it manually when done.")
    while True:
        time.sleep(1)

# Example usage:
cookie_files = [
    'twitter_cookies1.json', 
    'twitter_cookies2.json', 
    # 'twitter_cookies3.json'
]
post_url = 'https://twitter.com/peepoye_/status/1842170325519278473'  

main(cookie_files, post_url)
