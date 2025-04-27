import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
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
            self.assertIn('http', self.driver.current_url)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def test_section_anchors(self):
        self.driver.get(LOCAL_DOCS_URL)
        anchor_links = self.driver.find_elements(By.CSS_SELECTOR, '.nav-links a[href^="#"]')
        for link in anchor_links:
            target_id = link.get_attribute('href').split('#')[-1]
            if not target_id:
                continue
            link.click()
            time.sleep(0.5)
            # Check if the target section is now at the top of the viewport
            target_elem = self.driver.find_element(By.ID, target_id)
            self.assertTrue(target_elem.is_displayed())

if __name__ == '__main__':
    unittest.main()
