"""Scraper for Casa.it"""
from typing import List, Dict
from .base import BaseScraper
import re


class CasaitScraper(BaseScraper):
    """Scraper for Casa.it website."""

    def get_site_name(self) -> str:
        return "Casa.it"

    def build_search_url(self) -> str:
        """Build Casa.it search URL."""
        criteria = self.search_criteria

        # Casa.it URL structure for Monselice
        base_url = "https://www.casa.it/vendita/monselice"

        params = []

        # Price range
        params.append(f"prezzomin={criteria['price_min']}")
        params.append(f"prezzomax={criteria['price_max']}")

        # Area range
        params.append(f"superficiemin={criteria['area_min']}")
        params.append(f"superficiemax={criteria['area_max']}")

        # Rooms
        if criteria.get('rooms'):
            params.append(f"locali={criteria['rooms']}")

        url = base_url
        if params:
            url += "?" + "&".join(params)

        return url

    def parse_listing(self, listing_element) -> Dict:
        """Parse a single listing from Casa.it."""
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
            title_elem = listing_element.find('h2', class_='risultato-lista__title')
            if not title_elem:
                title_elem = listing_element.find('a', class_='risultato-lista__link')

            if title_elem:
                if title_elem.name == 'a':
                    listing['title'] = title_elem.get_text(strip=True)
                    listing['url'] = title_elem.get('href', '')
                else:
                    link = title_elem.find('a')
                    if link:
                        listing['title'] = link.get_text(strip=True)
                        listing['url'] = link.get('href', '')

                if listing['url'] and not listing['url'].startswith('http'):
                    listing['url'] = "https://www.casa.it" + listing['url']

            # Price
            price_elem = listing_element.find('div', class_='risultato-lista__price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_text = price_text.replace('€', '').replace('.', '').replace(',', '').strip()
                price_match = re.search(r'(\d+)', price_text)
                if price_match:
                    listing['price'] = int(price_match.group(1))

            # Area and rooms from features
            features_elem = listing_element.find('ul', class_='risultato-lista__features')
            if features_elem:
                features_text = features_elem.get_text()

                # Area
                area_match = re.search(r'(\d+)\s*m²', features_text)
                if area_match:
                    listing['area'] = int(area_match.group(1))

                # Rooms
                rooms_match = re.search(r'(\d+)\s*local', features_text, re.IGNORECASE)
                if rooms_match:
                    listing['rooms'] = int(rooms_match.group(1))

            # Location
            location_elem = listing_element.find('div', class_='risultato-lista__location')
            if location_elem:
                listing['location'] = location_elem.get_text(strip=True)

            # Description
            desc_elem = listing_element.find('div', class_='risultato-lista__description')
            if desc_elem:
                listing['description'] = desc_elem.get_text(strip=True)

            # Features
            full_text = listing_element.get_text().lower()
            for feature in self.search_criteria['features']:
                if feature.lower() in full_text:
                    listing['features'].append(feature)

            return listing

        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None

    def scrape(self) -> List[Dict]:
        """Scrape Casa.it for listings."""
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

        # Find all listing cards - Casa.it might use different class names
        listing_elements = soup.find_all('article', class_='risultato-lista')
        if not listing_elements:
            listing_elements = soup.find_all('div', class_='property-card')

        print(f"Found {len(listing_elements)} listings on page 1")

        for element in listing_elements:
            listing = self.parse_listing(element)
            if listing and listing.get('title'):
                if self.matches_criteria(listing):
                    listings.append(listing)
                    print(f"✓ Match found: {listing['title'][:50]}... - €{listing.get('price', 'N/A')}")

        # Try to scrape additional pages
        for page in range(2, 4):
            page_url = f"{url}&page={page}"
            soup = self.fetch_page(page_url)
            if not soup:
                break

            listing_elements = soup.find_all('article', class_='risultato-lista')
            if not listing_elements:
                listing_elements = soup.find_all('div', class_='property-card')

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
