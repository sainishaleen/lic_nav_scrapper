import time
import logging
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def select_date_from_calendar(driver, target_date):
    # Click the calendar icon to open the calendar
    calendar_button = driver.find_element(By.ID, "MainContent_imgbtncalender")
    calendar_button.click()

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "MainContent_CALnavdate")))

    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            calendar_header = driver.find_element(By.XPATH, "//td[@colspan='7']//table//td[contains(@style, 'width:70%')]")
            current_month_year = calendar_header.text.strip()

            target_month = target_date.strftime("%B")
            target_year = target_date.strftime("%Y")
            target_month_year = f"{target_month} {target_year}"

            while current_month_year != target_month_year:
                current_date_obj = datetime.strptime(current_month_year, "%B %Y")
                target_date_obj = datetime.strptime(target_month_year, "%B %Y")

                if target_date_obj > current_date_obj:
                    next_button = driver.find_element(By.XPATH, "//a[contains(@title, 'Go to the next month')]")
                    next_button.click()
                elif target_date_obj < current_date_obj:
                    prev_button = driver.find_element(By.XPATH, "//a[contains(@title, 'Go to the previous month')]")
                    prev_button.click()

                time.sleep(1)
                calendar_header = driver.find_element(By.XPATH, "//td[@colspan='7']//table//td[contains(@style, 'width:70%')]")
                current_month_year = calendar_header.text.strip()

            target_day = target_date.strftime("%d").lstrip("0")
            day_button = driver.find_element(By.XPATH, f"//a[@title='{target_day} {target_month}']")
            day_button.click()
            break
        except StaleElementReferenceException:
            retries += 1
            logging.warning(f"Stale element encountered. Retrying... ({retries}/{max_retries})")
            time.sleep(2)

    if retries == max_retries:
        logging.error("Failed to select date from calendar after multiple retries.")
        raise Exception("Failed to select date from calendar.")
