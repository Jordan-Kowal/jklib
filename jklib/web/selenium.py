# coding: utf8
"""
Functions for using a headless-browser through Selenium
Classes:
    WebBrowser: Wrapper around any Selenium browser instance, that acts as a CONTEXT MANAGER
Functions:
    browser_options: Creates and returns an "Option" instance for Mozilla, based on our settings
    create_browser: Creates and returns a Selenium Firefox browser using our context manager
    transfer_cookies_to_requests: Creates and returns a Session from "requests" and gets cookies from our browser
    write_in_field: Writes data in a field, and potentially clears it beforehand
"""


# Third-party
from requests import Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class WebBrowser:
    """
    Wrapper around any Selenium browser instance, that acts as a CONTEXT MANAGER
    Adds a 2s implicit wait time (maximum time to find elements on the page)
    Returns:
        WebBrowser: The class returns a WebBrowser instance
        SeleniumBrowser: The "with" statement return the actual selenium-supported browser instance
    """

    def __init__(self, browser):
        """
        Creates a class instance and sets up its attributes
        Args:
            browser (SeleniumBrowser): One of the selenium-supported browser instance
        """
        self.browser = browser
        self.browser.implicitly_wait(2)

    def __enter__(self):
        """
        Allows our class to be used as a context manager
        Returns a browser with the "WITH" statement
        Returns:
            (SeleniumBrowser) The instance's selenium-supported browser instance
        """
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit method for our context manager
        Will be run automatically when exiting the with statement (with or without error)
        Args:
            exc_type (?): Automatically filled by Python
            exc_val (?): Automatically filled by Python
            exc_tb (?): Automatically filled by Python
        """
        self.browser.quit()


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def browser_options(option_list):
    """
    Creates and returns an "Option" instance for Mozilla, based on our settings
    Args:
        option_list (list): list of command-line arguments (as string) for Firefox
    Returns:
        (Option) Option instance (from Selenium), that we will use when launching Firefox
    """
    options = Options()
    for arg in option_list:
        options.add_argument(arg)
    return options


def create_browser(browser_cls, options=None):
    """
    Creates and returns a Selenium Firefox browser using our context manager
    Args:
        browser_cls (*): Context manager for a browser object
        options (list, optional): List of strings that are "command-line args" for our browser. Defaults to None.
    Returns:
        (Firefox) Our Firefox browser instance
    """
    if options is None:
        options = []
    params = {
        "executable_path": "",
        "log_path": "",
        "options": browser_options(options),
    }
    with browser_cls(Firefox(**params)) as browser:
        return browser


def transfer_cookies_to_requests(browser):
    """
    Creates and returns a Session from "requests" and gets cookies from our browser
    Args:
        browser (Firefox): Selenium's Firefox instance, our current browser
    Returns:
        (Session) A Session instance
    """
    with Session() as session:
        for cookie in browser.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])
        return session


def write_in_field(field, text, clear=True):
    """
    Writes data in a field, and potentially clears it beforehand
    Args:
        field (FirefoxWebElement): HTML element from the page (from Selenium)
        text (str): Text we want to put in the field/input
        clear (bool, optional): Clears the field before writing our "text". Defaults to True.
    """
    if clear:
        field.clear()
    field.send_keys(text)
