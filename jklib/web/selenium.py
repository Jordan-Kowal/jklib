"""Utility functions for using a headless-browser through Selenium"""


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
        :param SeleniumBrowser browser: One of the selenium-supported browser instance
        """
        self.browser = browser
        self.browser.implicitly_wait(2)

    def __enter__(self):
        """
        Allows our class to be used as a context manager
        Returns a browser with the "WITH" statement
        :return: The instance's selenium-supported browser instance
        :rtype: SeleniumBrowser
        """
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit method for our context manager
        :param exc_type: Automatically filled by Python
        :param exc_val: Automatically filled by Python
        :param exc_tb: Automatically filled by Python
        """
        self.browser.quit()


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def browser_options(option_list):
    """
    Creates and returns an "Option" instance for Mozilla, based on our settings
    :param option_list: list of command-line arguments for Firefox
    :type option_list: list(str)
    :return: Option instance from Selenium that we will use when launching Firefox
    :rtype: Option
    """
    options = Options()
    for arg in option_list:
        options.add_argument(arg)
    return options


def create_browser(browser_cls, options=None):
    """
    Creates and returns a Selenium Firefox browser using our context manager
    :param browser_cls: Context manager for a browser object
    :param list options: List of strings that are "command-line args" for our browser. Defaults to None.
    :return: Our Firefox browser instance
    :rtype: Firefox
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
    :param Firefox browser: Selenium's Firefox instance, our current browser
    :return: A Session instance
    :rtype: Session
    """
    with Session() as session:
        for cookie in browser.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])
        return session


def write_in_field(field, text, clear=True):
    """
    Writes data in a field, and potentially clears it beforehand
    :param FirefoxWebElement field: HTML element from the page (from Selenium)
    :param str text: Text we want to put in the field/input
    :param bool clear: Whether to the field before writing our "text". Defaults to True.
    """
    if clear:
        field.clear()
    field.send_keys(text)
