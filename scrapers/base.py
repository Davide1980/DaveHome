"""Base scraper class for real estate websites."""
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time
import random


class BaseScraper(ABC):
    """Abstract base class for real estate scrapers."""

    def __init__(self, config: Dict):
        self.config = config
        self.search_criteria = config['search_criteria']
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

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

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch a page and return BeautifulSoup object."""
        try:
            # Random delay to be polite
            time.sleep(random.uniform(1, 3))

            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
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
