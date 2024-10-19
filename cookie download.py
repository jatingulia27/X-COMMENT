import json
from selenium import webdriver
import time

# Function to save cookies to a file after login
def save_cookies_to_file(driver, cookie_file_path):
    cookies = driver.get_cookies()  # Extract cookies from the current browser session
    with open(cookie_file_path, 'w') as cookie_file:
        json.dump(cookies, cookie_file)  # Save cookies to a JSON file
    print(f"Cookies saved to {cookie_file_path}")

# Function to log into Twitter manually and save cookies
def login_and_save_cookies():
    # Path to ChromeDriver (make sure to replace it with your actual path)
    driver = webdriver.Chrome()

    try:
        # Open the login page
        driver.get('https://twitter.com/login')
        print("Please log in manually within the next 60 seconds...")

        # Allow some time for manual login
        time.sleep(60)  # You can increase this if needed

        # After login, save the cookies
        save_cookies_to_file(driver, 'twitter_cookies.json')

    finally:
        driver.quit()  # Close the browser

# Run the login function
login_and_save_cookies()
