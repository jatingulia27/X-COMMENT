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

def interact_with_post(driver, post_url, comment_text):
    try:
        driver.get(post_url)
        print(f"Navigated to the post URL: {post_url}")

        time.sleep(5)  # Give time for the post to load

        # Comment on the post
        try:
            comment_box = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
            comment_box.click()
            comment_box.send_keys(comment_text)
            print("Comment typed")
        except Exception as e:
            print("Error finding comment box: ", e)

        # Post the comment
        try:
            tweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
            tweet_button.click()
            print("Comment posted successfully!")
        except Exception as e:
            print("Error posting comment: ", e)

        time.sleep(1)

        # Like the post
        try:
            like_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]')
            like_button.click()
            print("Post liked.")
        except Exception as e:
            print("Error liking the post: ", e)

        time.sleep(1)

        # Retweet the post
        try:
            retweet_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="retweet"]')
            retweet_button.click()
            print("Retweet button clicked. Waiting for confirmation...")

            time.sleep(1)  # Wait for retweet confirmation dialog to appear
            
            # Confirm retweet
            confirm_retweet = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="retweetConfirm"]')
            confirm_retweet.click()
            print("Post retweeted.")
        except Exception as e:
            print("Error during retweeting: ", e)

    except Exception as e:
        print(f"An error occurred while interacting with the post: {e}")

# Main function to open the browser and set up cookies for multiple accounts
def main(cookie_files, post_url):
    driver = webdriver.Chrome()
    try:
        comment_text = "sad"
        for cookie_file in cookie_files:
            print(f"\nUsing cookies from: {cookie_file}")
            driver.get('https://twitter.com/login')

            load_cookies_from_file(driver, cookie_file)
            driver.refresh() 
            time.sleep(2)

            interact_with_post(driver, post_url, comment_text)  # Combined interaction

            # Clear cookies 
            driver.delete_all_cookies()
            print("Cookies cleared for the next account.")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")


# Example usage:
cookie_files = [
    'twitter_cookies.json', 
    # 'twitter_cookies2.json', 
    # 'twitter_cookies3.json'
]
post_url = 'https://twitter.com/peepoye_/status/1842170325519278473'  

main(cookie_files, post_url)
