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
        
        self.switch_to_propertyx()

        return self.driver

    def title(self):
        return self.driver.title

    def current_url(self):
        return self.driver.current_url
    
    def switch_to_propertyx(self):

        print("=" * 60)
        print("Searching PropertyX tab...")
        print("=" * 60)
        
        print(f"Found {len(self.driver.window_handles)} browser tabs.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            print(f"Title : {self.driver.title}")
            print(f"URL   : {self.driver.current_url}")
            
            print("-" * 60)

            url = self.driver.current_url.lower()

            if (
                "workdesk.property-x.asia" in url
                or "sales.property-x.asia" in url
):

                print("✅ PropertyX tab found!")

                return True
            
    
    def get_driver(self):
        return self.driver


def get_browser():
    browser = Browser()
    browser.connect()
    return browser