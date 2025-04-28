import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set this to the path where your docs site is served locally, e.g., 'file:///path/to/docs/index.html' or 'http://localhost:8000/docs/index.html'
LOCAL_DOCS_URL = 'file:///' + __import__('os').path.abspath('docs/index.html').replace('\\', '/')

class TestAllLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_nav_links(self):
        self.driver.get(LOCAL_DOCS_URL)
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, '.nav-links a')
        for link in nav_links:
            href = link.get_attribute('href')
            if href.startswith('#'):
                continue  # Skip anchor links
            # Open link in new tab
            self.driver.execute_script("window.open(arguments[0]);", href)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(1)
            self.assertTrue(
                self.driver.current_url.startswith(('http', 'file')),
                f"Unexpected URL: {self.driver.current_url}"
            )
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def is_top_in_viewport(self, element, offset=100):
        # Checks if the top of the element is visible in the viewport, allowing for a sticky header of 'offset' px
        return self.driver.execute_script('''
            var elem = arguments[0], offset = arguments[1];
            var rect = elem.getBoundingClientRect();
            return (
                rect.top >= offset &&
                rect.top <= (window.innerHeight || document.documentElement.clientHeight)
            );
        ''', element, offset)

    def test_section_anchors(self):
        self.driver.get(LOCAL_DOCS_URL)
        anchor_links = self.driver.find_elements(By.CSS_SELECTOR, '.nav-links a[href^="#"]')
        for link in anchor_links:
            target_id = link.get_attribute('href').split('#')[-1]
            if not target_id:
                continue
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            # Adjust for sticky headers if present
            self.driver.execute_script("window.scrollBy(0, -100);")
            try:
                link.click()
            except ElementClickInterceptedException:
                # Fallback to JS click if intercepted
                self.driver.execute_script("arguments[0].click();", link)
            time.sleep(0.5)
            # Check if the target section is now at the top of the viewport
            target_elem = self.driver.find_element(By.ID, target_id)
            self.assertTrue(target_elem.is_displayed(), f"Element #{target_id} is not displayed")
            self.assertTrue(self.is_top_in_viewport(target_elem), f"Element #{target_id} top is not visible in viewport")

if __name__ == '__main__':
    unittest.main()
