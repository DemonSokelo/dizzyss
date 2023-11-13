import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


        # Function to append the URL to the output file with line number
def append_url_with_line_number(output_file_path, extracted_url):
    # Open the file in read mode to check if it's empty
    with open(output_file_path, 'r') as f:
        lines = f.readlines()

    if not lines or lines[-1].strip() == '':
        # If the file is empty or the last line is empty, set line_number to 1
        line_number = 1
    else:
        # Otherwise, extract the line number from the last line and increment it
        line_number = int(lines[-1].split(":")[0]) + 1

    # Append the URL to the file with the line number
    with open(output_file_path, 'a') as f:
        f.write(f"{line_number}: {extracted_url}\n")

def process_webpage(url, output_file_path, username, password):
    # Set up Chrome options with headless mode
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--disable-gpu')# Use incognito mode
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Use ChromeDriverManager to get the executable path
    chrome_driver_path = ChromeDriverManager().install()

    chrome_service = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the "Start my 1 month trial" button
        start_trial_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="cta-link-button" and contains(text(), "Start my 1 month trial")]'))
        )

        # Click the "Start my 1 month trial" button
        start_trial_button.click()

        # Handle the login process
        login(driver, username, password)

        wait_for_url_contains(driver, 'billing')  # Adjust with a keyword present in the redirected URL

        response = requests.get(url)

            # Check if the request was successful (status code 200)
        if response.status_code == 200:
                # Use BeautifulSoup to parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract relevant information using BeautifulSoup and make requests as needed

                # Extracted URL
                extracted_url = driver.current_url

                # Append the URL to the output file with line number
                append_url_with_line_number(output_file_path, extracted_url)

    finally:
        driver.quit()

def wait_for_url_contains(driver, keyword):
    WebDriverWait(driver, 20).until(
        lambda driver: keyword in driver.current_url
    )

def login(driver, username, password):
    # Implement the login process here

    cb1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continue with email | username")]'))
    )
    cb1.click()

    # For example:
    type_text_slowly(driver, username, (By.XPATH, '//input[@data-testid="text-control-input" and @type="email"]'))


    time.sleep(3)

    cb2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continue")]'))
    )
    cb2.click()

    type_text_slowly(driver, password, (By.XPATH, '//input[@data-testid="text-control-input" and @type="password"]'))

    time.sleep(2)

    # Re-locate the "Log in" button after the page updates
    cb13 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All Cookies")]'))
    )
    cb13.click()
    time.sleep(3)

    cb3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="reg-continue-button" and @type="submit"]'))
        )
    cb3.click()

    time.sleep(10)



    # Introduce a random delay after clicking the button


def type_text_slowly(driver, text, locator):
    # Simulate typing text letter by letter
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    actions = ActionChains(driver)
    for char in text:
        actions.send_keys_to_element(element, char)
        actions.perform()
        time.sleep(random.uniform(0.01, 0.01))

# Example usage
website_url = 'https://picsart.com/discord-nitro-plan-trial/'  # Replace with your target URL
output_file_path = 'promos.txt'
username = 'ADD YOUR PICSART USERNAME'
password = 'ADD YOUR PICSART PASSWORD'

# Run the process multiple times with variations in delays
for _ in range(100):
    process_webpage(website_url, output_file_path, username, password)
