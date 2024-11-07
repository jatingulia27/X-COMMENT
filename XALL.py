import json
import random
import time
import logging
import sqlite3
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to load cookies from a file
def load_cookies_from_file(driver, cookie_file_path):
    try:
        with open(cookie_file_path, 'r') as cookie_file:
            cookies = json.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        logger.info(f"Cookies loaded from {cookie_file_path}")
    except Exception as e:
        logger.error(f"Error loading cookies: {e}")

# Function to interact with the profile or post based on URL type
def process_url(driver, url, comment_list):
    if 'status' in url:  # URL indicates a post
        comment_text = random.choice(comment_list)
        interact_with_post(driver, url, comment_text)
        return {'follow': 'No', 'retweet': 'Yes', 'comment': 'Yes', 'like': 'Yes'}
    else:  # URL indicates an account profile
        follow_account(driver, url)
        return {'follow': 'Yes', 'retweet': 'No', 'comment': 'No', 'like': 'No'}

# Function to follow an account
def follow_account(driver, account_url):
    try:
        driver.get(account_url)
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-testid, "follow")]'))
        )
        follow_button.click()
        logger.info("Followed the account.")
    except Exception as e:
        logger.error(f"Error following account: {e}")

# Function to interact with a post (like, retweet, comment)
def interact_with_post(driver, post_url, comment_text):
    try:
        driver.get(post_url)
        time.sleep(3)  # Wait for post to load

        # Comment
        try:
            comment_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
            )
            comment_box.send_keys(comment_text)
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]').click()
            logger.info("Comment posted.")
        except Exception as e:
            logger.error("Error posting comment: %s", e)
            time.sleep(1)

        # Like
        try:
            like_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="like"]'))
            )
            like_button.click()
            logger.info("Post liked.")
        except Exception as e:
            logger.error("Error liking post: %s", e)
            time.sleep(1)

        # Retweet
        try:
            retweet_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="retweet"]'))
            )
            retweet_button.click()
            retweet_confirm_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="retweetConfirm"]'))
            )
            retweet_confirm_button.click()
            logger.info("Post retweeted.")
        except Exception as e:
            logger.error("Error retweeting post: %s", e)
            time.sleep(1)

    except Exception as e:
        logger.error(f"Error interacting with post: {e}")

# Function to set up SQLite database
def setup_database():
    conn = sqlite3.connect('interactions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            url TEXT,
            follow TEXT,
            retweet TEXT,
            comment TEXT,
            like TEXT
        )
    ''')
    conn.commit()
    return conn

# Function to save interaction in the database
def save_interaction(conn, interaction_data):
    c = conn.cursor()
    c.execute('''
        INSERT INTO interactions (url, follow, retweet, comment, like)
        VALUES (?, ?, ?, ?, ?)
    ''', (interaction_data['url'], interaction_data['follow'], interaction_data['retweet'], interaction_data['comment'], interaction_data['like']))
    conn.commit()

# Main function
def main(cookie_files):
    # Read URLs from CSV
    # Read URLs from CSV, ensuring there are no BOM or unwanted characters
    with open('urls.csv', newline='', encoding='utf-8-sig') as f:  # 'utf-8-sig' removes BOM if present
        url_list = [row[0].strip() for row in csv.reader(f)]



    # Read comments from CSV
    with open('comments.csv', newline='') as f:
        comment_list = [row[0] for row in csv.reader(f)]

    # Set up the database
    conn = setup_database()

    # Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # WebDriver initialization
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Iterate over cookies and URLs
        for cookie_file in cookie_files:
            logger.info(f"Using cookies from: {cookie_file}")
            driver.get('https://twitter.com/login')
            load_cookies_from_file(driver, cookie_file)
            driver.refresh()

            for url in url_list:
                interaction_data = process_url(driver, url, comment_list)
                interaction_data['url'] = url  # Add the URL to the data
                save_interaction(conn, interaction_data)
                logger.info(f"Interaction completed for URL: {url} with details: {interaction_data}")
                
            driver.delete_all_cookies()
            time.sleep(2)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        driver.quit()
        conn.close()

# Example usage
cookie_files = ['twitter_cookies22.json']  # Replace with actual cookie file paths
main(cookie_files)
