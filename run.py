import json
import os
import random
import re
import sys
import time
import emailsender

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from logger import Logger

with open('config.json') as data_file:
    config = json.load(data_file)

def create_driver(headless):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1600x900')
    if headless:
        options.add_argument('headless')
    return webdriver.Chrome(chrome_options=options)

driver = create_driver(config['tool']['headless'])
log = Logger(driver)

def open_page():
    log.info('Entering webpage')
    driver.get("https://portalpacjenta.luxmed.pl/PatientPortal/Reservations/Reservation/Find?firstTry=True")
    assert "LUX MED" in driver.title
    log.screenshot('open_page')
    log.info('Lux med webpage opened')


def log_in(login, passwd):
    log.info('Logging in user with login {}', login)
    input_login = driver.find_element_by_css_selector("form#loginForm input#Login")
    input_login.clear()
    input_login.send_keys(login)
    input_login.send_keys(Keys.TAB)
    input_pass = driver.find_element_by_css_selector("form#loginForm input#Password")
    input_pass.send_keys(passwd)
    input_submit = driver.find_element_by_css_selector("form#loginForm input[type=submit]")
    input_submit.click()
    log.info('User "{}" logged in', login)


def select_service_group(service_group):
    log.screenshot('select_service_group')
    log.info('Selecting service group "{}"', service_group)
    driver.find_element_by_css_selector('a[datasubcategory*="{}"]'.format(service_group)).click()
    log.info('Service group "{}" successfully selected', service_group)


def select_appointment_button():
    try:
        log.info('Pressing "appointment" button')
        log.screenshot('select_appointment_button')
        driver.find_element_by_xpath("//a[contains(@class, 'activity_button')][contains(text(),'Wizyta')]").click()
    except NoSuchElementException as e:
        log.warn("Appointment page not available")


def select_service(service_name):
    if not service_name:
        return

    log.info('Selecting service: "{}"', service_name)
    select_value_in_dropdown(2, 0, service_name)
    log.screenshot('select_service')


def select_person(person_name):
    if not person_name:
        return

    log.info('Selecting person: "{}"', person_name)
    select_value_in_dropdown(2, 1, person_name)
    log.screenshot('select_person')


def select_location(location):
    if not location:
        return

    log.info('Selecting location: "{}"', location)
    select_value_in_dropdown(1, 1, location)
    log.screenshot('select_location')


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
    time.sleep(3)


def select_dates(start_date, stop_date):
    log.info('Selecting dates. From {}, to {}', start_date, stop_date)
    time_picker_input = driver.find_element_by_css_selector("#rangePicker")
    time_picker_input.clear()
    time_picker_input.send_keys(start_date + '  |  ' + stop_date)
    driver.find_element_by_css_selector("body").click()
    driver.find_element_by_css_selector("body").click()
    log.screenshot('select_dates')


def submit_search_form():
    log.info("Performing search")
    log.screenshot('submit_search_form')
    submit_button = driver.find_element_by_css_selector("input[type=submit]")
    submit_button.click()


def close_popup():
    try:
        log.screenshot('close_popup')
        driver.find_element_by_css_selector("div#__popup button.reject").click()
        log.info("Closing popup")
    except NoSuchElementException:
        log.info("Popup not found")


def get_hour_from_slot(slot):
    slot_time_text = slot.find_element_by_css_selector("td.hours").text
    hour = slot_time_text.split(':')[0]
    return int(hour)


def is_slot_between(slot, time_from, time_to):
    slot_hour = get_hour_from_slot(slot)
    return time_from <= slot_hour <= time_to


def any_free_slot(time_from, time_to):
    slots_elements = driver.find_elements_by_css_selector('.reserveTable tbody tr')
    log.info("Number of all slots: {}".format(len(slots_elements)))
    log.screenshot('any_free_slot')

    log.info("Applying time filters: from {} to {}", time_from, time_to)
    slots_elements = list(filter(lambda slot: is_slot_between(slot, time_from, time_to), slots_elements))

    log.info("Number of matching slots: {}".format(len(slots_elements)))
    return len(slots_elements) != 0


def sleep_for_a_moment():
    sleep_time = random.randint(1, 20)
    log.info("About to sleep for {} seconds".format(sleep_time))
    time.sleep(sleep_time)


def find_text(text):
    src = driver.page_source
    text_found = re.findall(r'{}'.format(text), src)
    return text_found


def print_success_ascii_art():
    with open('success-asci-art.txt', 'r') as art_file:
        print(art_file.read())

def perform_authentication():
    open_page()
    log_in(config['credentials']['luxmedUsername'], config['credentials']['luxmedPassword'])
    time.sleep(5)

def fill_in_search_form():
    select_service_group(config['search']['serviceGroup'])
    time.sleep(5)
    select_appointment_button()
    time.sleep(5)
    select_service(config['search']['service'])
    time.sleep(2)
    select_person(config['search']['person'])
    time.sleep(2)
    select_location(config['search']['location'])
    time.sleep(2)
    select_dates(config['search']['dateFrom'], config['search']['dateTo'])
    time.sleep(2)

def on_matching_slot_found():
    print_success_ascii_art()
    log.screenshot('free_slots_found')
    os.system("play ./sms_mario.wav")
    emailsender.send_email("on_matching_slot_found")
    
    # Open browser, log in and search
    headless = config['tool'].get('headless')
    openBrowserOnSuccess = config['tool'].get('openBrowserOnSuccess')
    if headless and openBrowserOnSuccess:
        log.info('Opening browser')
        global driver
        driver = create_driver(False)
        perform_authentication()
        fill_in_search_form()
        submit_search_form()
    
    sys.exit(0)

def perform_endless_search():
    perform_authentication()
    fill_in_search_form()

    while True:
        time.sleep(5)
        submit_search_form()
        time.sleep(3)
        close_popup()

        if any_free_slot(config['search']['timeFrom'], config['search']['timeTo']):
            on_matching_slot_found()

        sleep_for_a_moment()


def main():
    while True:
        try:
            perform_endless_search()
        except Exception as e:
            print(e)


main()
