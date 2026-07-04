from selenium import webdriver
from selenium.webdriver.edge.options import Options

class Browser:

    def __init__(self):
        self.driver = None

    def connect(self):
        options = Options()

        options.add_experimental_option(
            "debuggerAddress",
            "127.0.0.1:9222"
        )

        self.driver = webdriver.Edge(options=options)

        return self.driver

    def title(self):
        return self.driver.title

    def current_url(self):
        return self.driver.current_url


def get_browser():
    browser = Browser()
    browser.connect()
    return browser