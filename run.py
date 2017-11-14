import json
import os
import random
import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

def open_page():    
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

def select_service_group(service_group):
    driver.find_element_by_css_selector('a[datasubcategory*="{}"]'.format(service_group)).click()

def select_appointment_button():
    try:
        driver.find_element_by_xpath("//a[contains(@class, 'activity_button')][contains(text(),'Wizyta')]").click()
    except NoSuchElementException as e:
        print "Appointment page not available"

def select_service(service_name):
    if not service_name:
        return

    select_value_in_dropdown(2, 0, service_name)

def select_person(person_name):
    if not person_name:
        return

    time.sleep(2)
    select_value_in_dropdown(2, 1, person_name)

def select_location(location):
    if not location:
        return

    time.sleep(2)
    select_value_in_dropdown(1, 1, location)

def select_value_in_dropdown(column_index, selector_index, value_to_select):
    css_path = "form#advancedResevation div.column{} div.graphicSelectContainer".format(column_index)
    select_location_dropdown = driver.find_elements_by_css_selector(css_path)[selector_index]
    select_location_dropdown.click()
    select_location_search = driver.find_element_by_css_selector("input.search-select")
    select_location_search.clear()
    select_location_search.send_keys(value_to_select)
    select_location_checkbox = driver.find_element_by_css_selector("ul#__selectOptions li:not(.hidden)")
    select_location_checkbox.click()
    driver.find_element_by_css_selector("body").click()

def select_dates(start_date, stop_date):
    time.sleep(2)
    time_picker_input = driver.find_element_by_css_selector("#rangePicker")
    time_picker_input.clear()
    time_picker_input.send_keys(start_date + '  |  ' + stop_date)
    driver.find_element_by_css_selector("body").click()
    driver.find_element_by_css_selector("body").click()


def submit_search_form():
    time.sleep(5)
    print "Performing search"
    submit_button = driver.find_element_by_css_selector("input[type=submit]")
    submit_button.click()


def close_popup():
    time.sleep(2)
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


def load_config():
    with open('config.json') as data_file:
        return json.load(data_file)


def perform_endless_search(config):
    open_page()
    log_in(config["luxmedUsername"], config["luxmedPassword"])
    time.sleep(5)
    select_service_group(config["serviceGroup"])
    time.sleep(5)    
    select_appointment_button()
    time.sleep(5)    
    select_service(config["service"])
    select_person(config["person"])
    select_location(config["location"])
    select_dates(config["dateFrom"], config["dateTo"])

    while True:
        submit_search_form()
        close_popup()

        if any_free_slot():
            print "**** GOOOOOOT IT ****"
            os.system("play ./sms_mario.wav")
            break
            # driver.close()

        sleep_for_a_moment()

def main():
    config = load_config()
    while True:
        try:
            perform_endless_search(config)
        except Exception as e:
            print e

main()
