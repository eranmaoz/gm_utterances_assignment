from playwright.sync_api import sync_playwright
import pytest


@pytest.mark.parametrize(
    "temperature_value, expected_displayed_value, expected_error_message",
    [
        ("20", "20", None),
        ("16", "16", None),
        ("25", "25", None),
        ("30", "30", None),
        ("-5", "-5", None),
        ("1000", None, "Error: The provided temperature value is not supported. Please enter a valid temperature")
    ]
)
def test_temperature_change(temperature_value, expected_displayed_value, expected_error_message):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.gm.com")
            page.fill("#temperature-input", temperature_value)
            page.click("#submit-button")

            if expected_error_message:
                error_message = page.inner_text("#error-message")
                assert error_message == expected_error_message, f"Expected error message: '{expected_error_message}', but got: '{error_message}'"
            else:
                displayed_temperature = page.inner_text("#displayed-temperature")
                assert displayed_temperature == expected_displayed_value, f"Expected temperature: '{expected_displayed_value}', but got: '{displayed_temperature}'"

    finally:
        # Ensure the browser is closed after the test
        browser.close()
