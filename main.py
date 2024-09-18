import logging
from datetime import datetime, timedelta
from config.settings import companies, user_agents, base_download_dir
from utils.selenium_setup import setup_driver
from utils.downloader import download_nav_data, to_snake_case
import os
import random
import time

def check_and_download(company_name, start_date, end_date):
    driver = setup_driver(random.choice(user_agents))
    
    # Define the download directory for the company
    company_folder = os.path.join(base_download_dir, to_snake_case(company_name))
    os.makedirs(company_folder, exist_ok=True)

    try:
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        for date in date_range:
            file_name = f"{to_snake_case(company_name)}_{date.strftime('%d-%b-%y')}.xls"
            file_path = os.path.join(company_folder, file_name)

            if not os.path.exists(file_path):
                logging.info(f"File missing: {file_name}. Attempting to download.")
                try:
                    downloaded_file = download_nav_data(driver, company_name, date, company_folder)
                    if os.path.exists(downloaded_file):
                        logging.info(f"Successfully downloaded {file_name}")
                    else:
                        logging.error(f"Download failed for {file_name}.")
                except Exception as e:
                    logging.error(f"Error downloading for {company_name} on {date.strftime('%d-%b-%y')}: {e}")
                time.sleep(random.uniform(3, 6))  # Random sleep between requests
            else:
                logging.info(f"File already exists: {file_name}")
    finally:
        driver.quit()

def main():
    today = datetime.today()
    start_date = datetime(2024, 8, 1)

    for company in companies:
        logging.info(f"Starting data check for {company}")
        check_and_download(company, start_date, today)

if __name__ == "__main__":
    main()
