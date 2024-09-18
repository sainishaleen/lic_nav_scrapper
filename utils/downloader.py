import os
import time
import logging
import random
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.calendar_handler import select_date_from_calendar
from selenium.webdriver.support.ui import Select 

# Function to get the latest downloaded file
def get_latest_downloaded_file(download_dir):
    files = [f for f in os.listdir(download_dir) if f and os.path.isfile(os.path.join(download_dir, f))]
    if not files:
        raise Exception("No files found in the download directory.")
    
    paths = [os.path.join(download_dir, file) for file in files]
    return max(paths, key=os.path.getctime)

# Function to download NAV data for a specific company and date
def download_nav_data(driver, company_name, date, company_folder):
    logging.info(f"Navigating to site to download data for {company_name} on {date.strftime('%d-%b-%y')}")
    driver.get("https://www.lifeinscouncil.org/industry%20information/ListOfFundNAVs")

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "MainContent_drpselectinscompany")))

    # Select the company
    select_element = Select(driver.find_element(By.ID, "MainContent_drpselectinscompany"))
    select_element.select_by_visible_text(company_name)

    # Random sleep to simulate human behavior
    time.sleep(random.uniform(3, 6))

    # Select the correct date from the calendar
    select_date_from_calendar(driver, date)

    time.sleep(random.uniform(3, 6))

    # Click the "Get Data" button
    get_data_button = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btngetdetails")))
    get_data_button.click()

    # Click the download button
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "MainContent_lbtnxl")))
    driver.execute_script("arguments[0].click();", download_button)

    time.sleep(20)  # Wait for download to complete

    # Try to get the latest downloaded file in the global downloads folder
    global_download_dir = os.path.join(os.getcwd(), "downloads")
    
    try:
        downloaded_file = get_latest_downloaded_file(global_download_dir)  # Default download location
        logging.info(f"Downloaded file: {downloaded_file}")

        # Rename the file to the desired format
        new_file_name = f"{to_snake_case(company_name)}_{date.strftime('%d-%b-%y')}.xls"
        new_file_path = os.path.join(company_folder, new_file_name)
        
        os.rename(downloaded_file, new_file_path)
        logging.info(f"Renamed and saved the file as {new_file_path}")
        return new_file_path
    except Exception as e:
        logging.error(f"Error in renaming the file: {e}")
        raise

def to_snake_case(company_name):
    return company_name.lower().replace(" ", "_").replace("-", "_")
