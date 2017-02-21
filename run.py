import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def open_page():
    global driver
    driver = webdriver.PhantomJS()
    driver.get("https://portalpacjenta.luxmed.pl/PatientPortal/Reservations/Reservation/Find?firstTry=True")
    assert "LUX MED" in driver.title


def log_in(login, passwd):
    input_login = driver.find_element_by_css_selector("form#loginForm input#Login")
    input_login.clear()
    input_login.send_keys(login)
    input_login.send_keys(Keys.TAB)
    input_pass = driver.find_element_by_css_selector("form#loginForm input#Password")
    input_pass.send_keys(passwd)
    input_submit = driver.find_element_by_css_selector("form#loginForm input[type=submit]")
    input_submit.click()


def select_service(service_name):
    select_service_dropdown = driver.find_element_by_css_selector(
        "form#advancedResevation div.column2 div.graphicSelectContainer")
    select_service_dropdown.click()
    select_service_search = driver.find_element_by_css_selector("input.search-select")
    select_service_search.clear()
    select_service_search.send_keys(service_name)
    select_service_checkbox = driver.find_element_by_css_selector("ul#__selectOptions li:not(.hidden)")
    select_service_checkbox.click()
    driver.find_element_by_css_selector("body").click()


def submit_search_form():
    driver.find_element_by_css_selector("form#advancedResevation input[type=submit]").click()


def close_popup():
    time.sleep(5)
    try:
        driver.find_element_by_css_selector("div#__popup button.reject").click()
    except NoSuchElementException as e:
        print e


def find_person(person):
    src = driver.page_source
    text_found = re.findall(r'{}'.format(person), src)
    return text_found


open_page()
log_in("", "")
select_service("pediatry - w gabinecie dzieci ch")
submit_search_form()
close_popup()
print find_person('')

driver.close()
