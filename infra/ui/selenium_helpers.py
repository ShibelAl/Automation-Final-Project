"""
This file gathers all the useful Selenium imports and helper functions in one place to keep the
test scripts cleaner and more organized. Instead of repeatedly importing the same Selenium classes
across different files, we can just import what we need from here.
"""
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec

# export the commonly used Selenium classes and functions
__all__ = ["TimeoutException", "Keys", "By", "WebDriverWait", "ActionChains", "ec"]
