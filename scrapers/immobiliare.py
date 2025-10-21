"""Scraper for Immobiliare.it"""
from typing import List, Dict
from .base import BaseScraper
import re


class ImmobiliareScraper(BaseScraper):
    """Scraper for Immobiliare.it website."""

    def get_site_name(self) -> str:
        return "Immobiliare.it"

    def build_search_url(self) -> str:
        """Build Immobiliare.it search URL."""
        criteria = self.search_criteria

        # Immobiliare.it URL structure
        base_url = "https://www.immobiliare.it/vendita-case/monselice/"

        params = []

        # Price range
        params.append(f"prezzoMassimo={criteria['price_max']}")
        params.append(f"prezzoMinimo={criteria['price_min']}")

        # Area range
        params.append(f"superficieMinima={criteria['area_min']}")
        params.append(f"superficieMassima={criteria['area_max']}")

        # Rooms
        if criteria.get('rooms'):
            params.append(f"localiMinimo={criteria['rooms']}")

        # Property type - casa indipendente
        params.append("idCategoria=1")  # Residential
        params.append("idContratto=1")  # Sale

        url = base_url + "?" + "&".join(params)
        return url

    def parse_listing(self, listing_element) -> Dict:
        """Parse a single listing from Immobiliare.it."""
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

            # Title
            title_elem = listing_element.find('a', class_='in-card__title')
            if title_elem:
                listing['title'] = title_elem.get_text(strip=True)
                listing['url'] = "https://www.immobiliare.it" + title_elem.get('href', '')

            # Price
            price_elem = listing_element.find('li', class_='nd-list__item in-feat__item--main in-feat__item--price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'([\d.]+)', price_text.replace('.', ''))
                if price_match:
                    listing['price'] = int(price_match.group(1))

            # Area
            area_elem = listing_element.find('li', class_='in-feat__item--surface')
            if area_elem:
                area_text = area_elem.get_text(strip=True)
                area_match = re.search(r'(\d+)', area_text)
                if area_match:
                    listing['area'] = int(area_match.group(1))

            # Rooms
            rooms_elem = listing_element.find('li', class_='in-feat__item--rooms')
            if rooms_elem:
                rooms_text = rooms_elem.get_text(strip=True)
                rooms_match = re.search(r'(\d+)', rooms_text)
                if rooms_match:
                    listing['rooms'] = int(rooms_match.group(1))

            # Location
            location_elem = listing_element.find('div', class_='in-card__location')
            if location_elem:
                listing['location'] = location_elem.get_text(strip=True)

            # Description
            desc_elem = listing_element.find('div', class_='in-card__description')
            if desc_elem:
                listing['description'] = desc_elem.get_text(strip=True)

            # Features
            features_text = listing_element.get_text().lower()
            for feature in self.search_criteria['features']:
                if feature.lower() in features_text:
                    listing['features'].append(feature)

            return listing

        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None

    def scrape(self) -> List[Dict]:
        """Scrape Immobiliare.it for listings."""
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
        listing_elements = soup.find_all('div', class_='in-card')
        print(f"Found {len(listing_elements)} listings on page 1")

        for element in listing_elements:
            listing = self.parse_listing(element)
            if listing and listing.get('title'):
                if self.matches_criteria(listing):
                    listings.append(listing)
                    print(f"✓ Match found: {listing['title'][:50]}... - €{listing.get('price', 'N/A')}")

        # Try to scrape additional pages (up to 3 pages)
        for page in range(2, 4):
            page_url = f"{url}&pag={page}"
            soup = self.fetch_page(page_url)
            if not soup:
                break

            listing_elements = soup.find_all('div', class_='in-card')
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
