from behave import *
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TIMEOUT = 20

@given('the user is on the simple interest calculator screen')
def step_impl(context):
    time.sleep(5)  # Wait for app to fully load - initial wait
    pass # Assuming the app starts on this screen


@when('the user enters "{text}" into the principal input field')
def step_impl(context, text):
    principal_input = WebDriverWait(context.driver, TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@resource-id='principalInput']"))
    )
    principal_input.send_keys(text)

@when('the user enters "{text}" into the interest rate input field')
def step_impl(context, text):
    interest_rate_input = WebDriverWait(context.driver, TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@resource-id='interestRateInput']"))
    )
    interest_rate_input.send_keys(text)


@when('the user enters "{text}" into the period input field')
def step_impl(context, text):
    period_input = WebDriverWait(context.driver, TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@resource-id='periodInput']"))
    )
    period_input.send_keys(text)


@when('the user taps the calculate button')
def step_impl(context):
    calculate_button = WebDriverWait(context.driver, TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.Button[@resource-id='calculateButton']"))
    )
    calculate_button.click()


@then('the result should be "{expected_result}"')
def step_impl(context, expected_result):
    #  This part needs adjustment based on how the result is displayed in the app.
    # Assuming the result is displayed in a TextView with a specific resource-id.  Replace "resultTextView" if necessary.
    #  Also, you will need to extract the actual result from the TextView and compare it to the expected_result.
    
    # Example using a TextView with resource-id 'resultTextView'
    # result_textview = WebDriverWait(context.driver, TIMEOUT).until(
    #     EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@resource-id='resultTextView']"))
    # )
    # actual_result = result_textview.text  # Extract the actual result from the textview.
    # assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
    
    # Placeholder -  Replace with the actual implementation once the result display mechanism is clear.
    print("Result validation placeholder.  Implement this once the result display element is known.")
    # Example of comparing the result.  Assuming result is directly available as text:
    # assert context.driver.page_source.contains(expected_result), f"Expected {expected_result} in page source, but not found."