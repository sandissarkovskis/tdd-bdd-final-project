######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps for BDD tests using Selenium
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = 'product_'  # Make sure HTML uses this prefix
WAIT_TIME = 10  # default wait time for WebDriverWait

##################################################################
# Navigation Steps
##################################################################

@when('I visit the "Home Page"')
def step_visit_home_page(context):
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_check_title(context, message):
    assert message in context.driver.title

@then('I should not see "{text_string}"')
def step_check_not_in_body(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert text_string not in element.text

##################################################################
# Input field Steps
##################################################################

@when('I set the "{element_name}" to "{text_string}"')
def step_set_field(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@when('I change "{element_name}" to "{text_string}"')
def step_change_field(context, element_name, text_string):
    step_set_field(context, element_name, text_string)  # same as set

@when('I select "{text}" in the "{element_name}" dropdown')
def step_select_dropdown(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select = Select(WebDriverWait(context.driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, element_id))
    ))
    select.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_check_dropdown(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select = Select(context.driver.find_element(By.ID, element_id))
    assert select.first_selected_option.text == text

@then('the "{element_name}" field should be empty')
def step_check_empty_field(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == ''

##################################################################
# Clipboard simulation
##################################################################

@when('I copy the "{element_name}" field')
def step_copy_field(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value') or ''
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_paste_field(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

##################################################################
# Button Steps
##################################################################

@when('I press the "{button}" button')
def step_press_button(context, button):
    button_id = button.lower() + '-btn'
    element = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, button_id))
    )
    element.click()

##################################################################
# Result / Search Steps
##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_check_field_value(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    assert found

@then('I should see "{name}" in the results')
def step_check_results(context, name):
    found = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.text_to_be_present_in_element((By.ID, 'search_results'), name)
    )
    assert found

@then('I should not see "{name}" in the results')
def step_check_results_not(context, name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert name not in element.text

@then('I should see the message "{message}"')
def step_check_flash_message(context, message):
    found = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.text_to_be_present_in_element((By.ID, 'flash_message'), message)
    )
    assert found
