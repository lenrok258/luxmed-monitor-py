import random
import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def open_page():
    global driver
    driver = webdriver.Chrome()
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
    select_service_dropdown = driver.find_elements_by_css_selector(
        "form#advancedResevation div.column2 div.graphicSelectContainer")[0]
    select_service_dropdown.click()
    select_service_search = driver.find_element_by_css_selector("input.search-select")
    select_service_search.clear()
    select_service_search.send_keys(service_name)
    select_service_checkbox = driver.find_element_by_css_selector("ul#__selectOptions li:not(.hidden)")
    select_service_checkbox.click()
    driver.find_element_by_css_selector("body").click()


def select_person(person_name):
    time.sleep(2)
    select_person_dropdown = driver.find_elements_by_css_selector(
        "form#advancedResevation div.column2 div.graphicSelectContainer")[1]
    select_person_dropdown.click()
    select_person_search = driver.find_element_by_css_selector("input.search-select")
    select_person_search.clear()
    select_person_search.send_keys(person_name)
    select_person_checkbox = driver.find_element_by_css_selector("ul#__selectOptions li:not(.hidden)")
    select_person_checkbox.click()
    driver.find_element_by_css_selector("body").click()


def select_dates(start_date, stop_date):
    time.sleep(2)
    time_picker_input = driver.find_element_by_css_selector("#rangePicker")
    time_picker_input.clear()
    time_picker_input.send_keys(start_date + ' | ' + stop_date)
    driver.find_element_by_css_selector("body").click()
    driver.find_element_by_css_selector("body").click()


def submit_search_form():
    time.sleep(2)
    print "Performing search"
    submit_button = driver.find_element_by_css_selector("input[type=submit]")
    submit_button.click()


def close_popup():
    time.sleep(1)
    try:
        driver.find_element_by_css_selector("div#__popup button.reject").click()
    except NoSuchElementException as e:
        print e


def any_free_slot():
    slots_elements = driver.find_elements_by_css_selector('.reserveTable')
    print "Free slots found: {}".format(slots_elements)
    return len(slots_elements) != 0


def sleep_for_a_moment():
    sleep_time = random.randint(1, 20)
    print "About to sleep for {} seconds".format(sleep_time)
    time.sleep(sleep_time)


def find_text(text):
    src = driver.page_source
    text_found = re.findall(r'{}'.format(text), src)
    return text_found


def main():
    open_page()
    log_in("", "")
    select_service("internisty")
    select_person(u"W\u0118GRZYN")
    select_dates('10-03-2017', '10-03-2017')
    while True:
        submit_search_form()
        close_popup()
        sleep_for_a_moment()
        if any_free_slot():
            print "GOOOOOOT IT !!!!!!!!!"
            break

            # driver.close()


main()
