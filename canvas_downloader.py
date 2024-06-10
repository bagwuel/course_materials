import requests
import zipfile
import os
import shutil
import time
import re
import subprocess
import sys

# Check if Selenium is installed, and install it if not
try:
    import selenium
    print("Selenium is installed.")
except ImportError:
    print("Selenium is not installed. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    print("Selenium has been installed.")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

if not os.path.isfile('chromedriver.exe'):
    # URL of the file to be downloaded
    chrome_driver_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/win64/chromedriver-win64.zip'

    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to save the downloaded file
    zip_file_path = os.path.join(script_dir, 'chromedriver-win64.zip')

    # Download the file
    response = requests.get(chrome_driver_url)
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)

    print(f"Downloaded {zip_file_path}")

    # Path to extract the contents
    extract_dir = os.path.join(script_dir, 'chromedriver_temp')

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Extracted to {extract_dir}")

    # Move the chromedriver executable to the current directory
    extracted_executable_path = os.path.join(extract_dir, 'chromedriver-win64\\chromedriver.exe')
    final_executable_path = os.path.join(script_dir, 'chromedriver.exe')
    shutil.move(extracted_executable_path, final_executable_path)

    print(f"Moved {extracted_executable_path} to {final_executable_path}")

    # Clean up by removing the downloaded zip file
    os.remove(zip_file_path)
    print(f"Removed {zip_file_path}")

    # Remove the old folder containing the executable
    shutil.rmtree(extract_dir)
    print(f"Removed {extract_dir}")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


USERNAME = 'school email'
PASSWORD = 'password'


try:
    # Navigate to the login page
    driver.get('https://canvas.hull.ac.uk')

    email_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0116')))
    email_element.send_keys(USERNAME)

    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    next_button.click()

    password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0118')))
    password_element.send_keys(PASSWORD)

    # Click the sign-in button
    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    sign_in_button.click()

    try:
        # Wait for the 2FA approval screen
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idDiv_SAOTCAS_Title')))
        print("Approve the sign-in request in your Authenticator app.")

        # Polling to wait for approval (adjust timeout as necessary)
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'idDiv_SAOTCAS_Title')))
    except:
        print("2FA step not found or already approved.")
    
    # Proceed after 2FA approval

    # Stay signed in
    try:
        stay_signed_in_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
        stay_signed_in_button.click()
    except TimeoutException:
        print("Stay signed in prompt not shown")

    WebDriverWait(driver, 20).until(EC.url_contains('https://canvas.hull.ac.uk'))
    driver.get('https://canvas.hull.ac.uk/courses')

    # Wait for the courses page to load and get all link hrefs
    links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    hrefs = [{link.text : link.get_attribute('href')} for link in links if link.get_attribute('href')]

    pattern = re.compile(r'\d{4,}$')
    filtered_hrefs = [href for href in hrefs if any(pattern.search(url) for url in href.values())]


    def find_div_elements(driver):
        try:
            div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.item-group-condensed.context_module')
            return [div for div in div_elements if 'Week' in div.get_attribute('aria-label')]
        except NoSuchElementException:
            return []
    

    for href in filtered_hrefs:
        for key, value in href.items():
            print(key, value)
            driver.get(value)
            div_elements = find_div_elements(driver)
            if div_elements:
                print('yeehh!!', key)
                main_folder = key.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                os.makedirs(main_folder, exist_ok=True)
                aria_labels = [div.get_attribute('aria-label') for div in div_elements]
                for i in range(len(div_elements)):
                    driver.get(value)
                    try:
                        # Properly format the CSS selector with the aria-label value
                        div = driver.find_element(By.CSS_SELECTOR, f'div[aria-label="{aria_labels[i]}"]')
                        folder_name = div.get_attribute('aria-label')
                        folder_name = folder_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                        subfolder = os.path.join(main_folder, folder_name)
                        os.makedirs(subfolder, exist_ok=True)
                        anchor_tags = div.find_elements(By.TAG_NAME, 'a')
                        resources = [tag.get_attribute('href') for tag in anchor_tags if len(anchor_tags) > 0]
                        filtered_resources = [resource for resource in resources if resource and pattern.search(resource)]

                        for resource in filtered_resources:
                            print(folder_name, resource)
                            driver.get(resource)
                            download_anchors = driver.find_elements(By.CSS_SELECTOR, 'a[download]')
                            filtered_links = [(anchor.get_attribute('href'), anchor.text) for anchor in download_anchors if 'download' in anchor.get_attribute('href')]
                            for href, anchor_text in filtered_links:
                                print(resource, anchor_text, href)
                                filename = anchor_text.strip()
                                filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                                
                                # Define the complete file path
                                filepath = os.path.join(subfolder, filename)
                                response = requests.get(href)
                                if response.status_code == 200:
                                    with open(filepath, 'wb') as file:
                                        file.write(response.content)
                                    print(f"Downloaded: {filepath}")
                                else:
                                    print(f"Failed to download: {filepath}")
                    except NoSuchElementException:
                        print(f"No div found with aria-label: {aria_labels[i]}")
                    print('\n\n')

finally:
    time.sleep(10)
    # Close the browser
    driver.quit()
