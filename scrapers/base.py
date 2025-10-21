"""Base scraper class for real estate websites."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class BaseScraper(ABC):
    """Abstract base class for real estate scrapers."""

    def __init__(self, config: Dict):
        self.config = config
        self.search_criteria = config['search_criteria']
        self.results = []
        self.driver: Optional[webdriver.Chrome] = None

    @abstractmethod
    def build_search_url(self) -> str:
        """Build the search URL based on criteria."""
        pass

    @abstractmethod
    def parse_listing(self, listing_element) -> Dict:
        """Parse a single listing element."""
        pass

    @abstractmethod
    def get_site_name(self) -> str:
        """Return the name of the website."""
        pass

    def init_driver(self):
        """Initialize the Chrome driver with anti-detection options."""
        if self.driver is None:
            try:
                options = Options()

                # Anti-detection options
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--lang=it-IT')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

                # Set realistic user agent
                options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

                # Initialize driver
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)

                # Execute CDP commands to hide webdriver
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                print(f"✓ Browser initialized for {self.get_site_name()}")
            except Exception as e:
                print(f"Error initializing driver: {e}")
                self.driver = None

    def close_driver(self):
        """Close the Chrome driver."""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except Exception as e:
                print(f"Error closing driver: {e}")

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch a page using Selenium and return BeautifulSoup object."""
        try:
            # Initialize driver if not already done
            if self.driver is None:
                self.init_driver()

            if self.driver is None:
                return None

            # Random delay to be polite
            time.sleep(random.uniform(2, 4))

            # Navigate to the URL
            self.driver.get(url)

            # Wait for page to load
            time.sleep(random.uniform(3, 5))

            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            return BeautifulSoup(page_source, 'lxml')

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def matches_criteria(self, listing: Dict) -> bool:
        """Check if a listing matches the search criteria."""
        criteria = self.search_criteria

        # Check price
        if listing.get('price'):
            price = listing['price']
            if price < criteria['price_min'] or price > criteria['price_max']:
                return False

        # Check area
        if listing.get('area'):
            area = listing['area']
            if area < criteria['area_min'] or area > criteria['area_max']:
                return False

        # Check rooms
        if listing.get('rooms') and criteria.get('rooms'):
            if listing['rooms'] < criteria['rooms']:
                return False

        return True

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Main scraping method."""
        pass
