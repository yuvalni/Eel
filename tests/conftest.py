import os
from unittest import mock

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


@pytest.fixture
def driver():
    TEST_BROWSER = os.environ.get("TEST_BROWSER", "chrome").lower()

    if TEST_BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        capabilities = DesiredCapabilities.FIREFOX
        capabilities['loggingPrefs'] = {"browser": "ALL"}

        driver = webdriver.Firefox(options=options, capabilities=capabilities, service_log_path=os.path.devnull)

    elif TEST_BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = True
        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {"browser": "ALL"}

        driver = webdriver.Chrome(options=options, desired_capabilities=capabilities, service_log_path=os.path.devnull)

    else:
        raise ValueError(f"Unsupported browser for testing: {TEST_BROWSER}")

    with mock.patch("eel.browsers.open"):
        yield driver
