"""Scraper for Subito.it"""
from typing import List, Dict
from .base import BaseScraper
import re


class SubitoScraper(BaseScraper):
    """Scraper for Subito.it website."""

    def get_site_name(self) -> str:
        return "Subito.it"

    def build_search_url(self) -> str:
        """Build Subito.it search URL."""
        criteria = self.search_criteria

        # Subito.it URL structure
        base_url = "https://www.subito.it/annunci-veneto/vendita/immobili/padova/monselice/"

        params = []

        # Price range
        params.append(f"ps={criteria['price_min']}")
        params.append(f"pe={criteria['price_max']}")

        # Area range (if supported)
        params.append(f"ss={criteria['area_min']}")
        params.append(f"se={criteria['area_max']}")

        url = base_url
        if params:
            url += "?" + "&".join(params)

        return url

    def parse_listing(self, listing_element) -> Dict:
        """Parse a single listing from Subito.it."""
        try:
            listing = {
                'source': self.get_site_name(),
                'title': None,
                'price': None,
                'area': None,
                'rooms': None,
                'location': None,
                'description': None,
                'url': None,
                'features': []
            }

            # Title and URL
            title_elem = listing_element.find('h2', class_='ItemTitle')
            if not title_elem:
                title_elem = listing_element.find('a', class_='SmallCard-module_link')

            if title_elem:
                link = title_elem if title_elem.name == 'a' else title_elem.find('a')
                if link:
                    listing['title'] = link.get_text(strip=True)
                    href = link.get('href', '')
                    if href and not href.startswith('http'):
                        listing['url'] = "https://www.subito.it" + href
                    else:
                        listing['url'] = href

            # Price
            price_elem = listing_element.find('p', class_='price')
            if not price_elem:
                price_elem = listing_element.find('div', class_='SmallCard-module_price')

            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_text = price_text.replace('€', '').replace('.', '').replace(',', '').strip()
                price_match = re.search(r'(\d+)', price_text)
                if price_match:
                    listing['price'] = int(price_match.group(1))

            # Location
            location_elem = listing_element.find('span', class_='town')
            if not location_elem:
                location_elem = listing_element.find('span', class_='SmallCard-module_city')

            if location_elem:
                listing['location'] = location_elem.get_text(strip=True)

            # Description and features extraction
            desc_elem = listing_element.find('p', class_='description')
            if not desc_elem:
                desc_elem = listing_element.find('div', class_='SmallCard-module_description')

            if desc_elem:
                listing['description'] = desc_elem.get_text(strip=True)

            # Extract area and rooms from description or title
            full_text = listing_element.get_text()

            # Area
            area_match = re.search(r'(\d+)\s*m[q²]', full_text, re.IGNORECASE)
            if area_match:
                listing['area'] = int(area_match.group(1))

            # Rooms
            rooms_match = re.search(r'(\d+)\s*(?:camere|local|vani)', full_text, re.IGNORECASE)
            if rooms_match:
                listing['rooms'] = int(rooms_match.group(1))

            # Features
            full_text_lower = full_text.lower()
            for feature in self.search_criteria['features']:
                if feature.lower() in full_text_lower:
                    listing['features'].append(feature)

            return listing

        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None

    def scrape(self) -> List[Dict]:
        """Scrape Subito.it for listings."""
        print(f"\n{'='*60}")
        print(f"Starting scraping: {self.get_site_name()}")
        print(f"{'='*60}")

        url = self.build_search_url()
        print(f"Search URL: {url}")

        soup = self.fetch_page(url)
        if not soup:
            print(f"Failed to fetch {self.get_site_name()}")
            self.close_driver()
            return []

        listings = []

        # Find all listing cards
        listing_elements = soup.find_all('div', class_='item-card')
        if not listing_elements:
            listing_elements = soup.find_all('div', class_='SmallCard-module_container')
        if not listing_elements:
            listing_elements = soup.find_all('article', class_='items__item')

        print(f"Found {len(listing_elements)} listings on page 1")

        for element in listing_elements:
            listing = self.parse_listing(element)
            if listing and listing.get('title'):
                if self.matches_criteria(listing):
                    listings.append(listing)
                    print(f"✓ Match found: {listing['title'][:50]}... - €{listing.get('price', 'N/A')}")

        # Try to scrape additional pages
        for page in range(2, 4):
            page_url = f"{url}&o={page}"
            soup = self.fetch_page(page_url)
            if not soup:
                break

            listing_elements = soup.find_all('div', class_='item-card')
            if not listing_elements:
                listing_elements = soup.find_all('div', class_='SmallCard-module_container')
            if not listing_elements:
                listing_elements = soup.find_all('article', class_='items__item')

            if not listing_elements:
                break

            print(f"Found {len(listing_elements)} listings on page {page}")

            for element in listing_elements:
                listing = self.parse_listing(element)
                if listing and listing.get('title'):
                    if self.matches_criteria(listing):
                        listings.append(listing)
                        print(f"✓ Match found: {listing['title'][:50]}... - €{listing.get('price', 'N/A')}")

        print(f"Total matches from {self.get_site_name()}: {len(listings)}")
        self.close_driver()
        return listings
