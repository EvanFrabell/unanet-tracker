import calendar
import datetime
import os
import time

import chromedriver_autoinstaller
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument(f'--headless')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sierra7.unanet.biz/sierra7/action/home")

# For developers:
# with open("C:\\Users\\epfra\\Documents\\GitHub\\credentials_self.yaml", "r") as yaml_file:
#     data = yaml.safe_load(yaml_file)

with open("credentials.yaml", "r") as yaml_file:
    data = yaml.safe_load(yaml_file)

user = data['credentials']['username']
password = data['credentials']['password']
project_name = 'T4NG_043_PAAS_Y02'


def login():
    # Replace time with WebDriver.Wait, time package is more dependable if you aren't in a rush
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(user)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@name='passwd']").send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(5)

    for x in range(2):
        # MFA call option
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Call')]"))).click()
        time.sleep(45)

        unauthorized = driver.find_elements(By.XPATH, "//a[@id='signInAnotherWay']")
        if x == 2:
            return False
        elif len(unauthorized) > 0:
            driver.find_element(By.XPATH, "//a[@id='signInAnotherWay']").click()
            print('Log-in Failed. Retry Once.')
        else:
            print('Authorized log-in')
            return True


def create_timesheet():
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Create Timesheet']"))).click()
    time.sleep(4)
    # button = driver.find_element(By.XPATH, "//button[@id='button_save']")
    # driver.execute_script("arguments[0].scrollIntoView();", button)
    # button.click()
    # time.sleep(3)
    # Return home may be unnecessary.  Unable to test function in production.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Home']"))).click()

    # time.sleep(3) WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@title,
    # 'Edit timesheet')]"))).click() time.sleep(3)
    #
    # driver.find_element(By.XPATH, "(//tr//td[@class='project'])[1]").click()
    # time.sleep(1)
    # driver.find_element(By.XPATH, f"(//div[contains(.,'{project_name}')])[last()]").click()
    # time.sleep(3)


def edit_timesheet(day_month):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Current Timesheet')]"))).click()
    time.sleep(3)

    time_rows = driver.find_elements(By.XPATH, "//table[@id='timesheet']//tbody//tr")
    time.sleep(2)
    for row in time_rows:
        title = row.get_attribute('title')

        project_codes = ('OVERHEAD', 'Start typing in', 'LWOP', 'PTO')
        if any(s in title for s in project_codes) or title == '':
            continue

        xpath = f"//table[@id='timesheet']//tbody//tr[@title='{title}']//td[@id='d_3_{day_month}']//input"
        driver.find_element(By.XPATH, xpath).send_keys(8)
    time.sleep(4)

    button = driver.find_element(By.XPATH, "//button[@id='button_save']")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(6)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Home']"))).click()


def submit_timesheet():
    # driver.find_element(By.XPATH, "//button[@name='button_submit']").click()
    print('Timesheet submitted!')


if __name__ == '__main__':
    today = datetime.date.today()
    # (0 = Monday, 1 = Tuesday, 4 = Friday, 6 = Sunday)
    day_of_week = today.weekday()
    day_of_month = today.day
    month = datetime.date.today().month
    year = datetime.date.today().year
    last_day_of_month = calendar.monthrange(year, month)[1]

    login_successful = False

    # If user sets scheduler for weekends it will continue to skip
    if day_of_week in (5, 6):
        print('Skip today.')
    else:
        login_successful = login()

    if login_successful:
        time_sheet = driver.find_element(By.XPATH, "(//div[@id='active-timesheet-list']//tr)[2]").text

        if 'There are no' in time_sheet:
            print('Create TimeSheet')
            create_timesheet()
            time.sleep(3)
            edit_timesheet(day_of_month)
            print('TimeSheet Complete.')
        else:
            edit_timesheet(day_of_month)
            print('TimeSheet Complete.')

            if day_of_month == 15 or (day_of_week == 4 and day_of_month in (13, 14)):
                submit_timesheet()
            if day_of_month == last_day_of_month or (day_of_week == 4 and (
                    day_of_month + 1 == last_day_of_month or day_of_month + 2 == last_day_of_month)):
                submit_timesheet()

        driver.quit()
    else:
        driver.quit()
