#!/usr/bin/env python3
"""Main script to scrape multiple real estate websites."""

import json
import pandas as pd
from datetime import datetime
from scrapers.immobiliare import ImmobiliareScraper
from scrapers.casait import CasaitScraper
from scrapers.idealista import IdealistaScraper
from scrapers.subito import SubitoScraper


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_results(all_results, output_config):
    """Save results to CSV file."""
    if not all_results:
        print("\nNo results to save.")
        return

    df = pd.DataFrame(all_results)

    # Reorder columns for better readability
    columns_order = ['source', 'title', 'price', 'area', 'rooms', 'location', 'features', 'url', 'description']
    existing_columns = [col for col in columns_order if col in df.columns]
    df = df[existing_columns]

    # Sort by price
    if 'price' in df.columns:
        df = df.sort_values('price')

    # Add timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = output_config['filename'].replace('.csv', f'_{timestamp}.csv')

    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n{'='*60}")
    print(f"Results saved to: {filename}")
    print(f"{'='*60}")

    return filename


def print_summary(all_results):
    """Print summary of results."""
    if not all_results:
        print("\nNo results found.")
        return

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")

    # Count by source
    sources = {}
    for result in all_results:
        source = result['source']
        sources[source] = sources.get(source, 0) + 1

    print(f"\nTotal properties found: {len(all_results)}")
    print("\nBy source:")
    for source, count in sources.items():
        print(f"  - {source}: {count}")

    # Price statistics
    prices = [r['price'] for r in all_results if r.get('price')]
    if prices:
        print(f"\nPrice range:")
        print(f"  - Min: €{min(prices):,}")
        print(f"  - Max: €{max(prices):,}")
        print(f"  - Average: €{int(sum(prices)/len(prices)):,}")

    # Area statistics
    areas = [r['area'] for r in all_results if r.get('area')]
    if areas:
        print(f"\nArea range:")
        print(f"  - Min: {min(areas)} m²")
        print(f"  - Max: {max(areas)} m²")
        print(f"  - Average: {int(sum(areas)/len(areas))} m²")

    # Top 5 matches
    print(f"\n{'='*60}")
    print("TOP 5 MATCHES:")
    print(f"{'='*60}")

    sorted_results = sorted(all_results, key=lambda x: x.get('price', float('inf')))
    for i, result in enumerate(sorted_results[:5], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Source: {result['source']}")
        print(f"   Price: €{result.get('price', 'N/A'):,}" if result.get('price') else "   Price: N/A")
        print(f"   Area: {result.get('area', 'N/A')} m²")
        print(f"   Rooms: {result.get('rooms', 'N/A')}")
        print(f"   Location: {result.get('location', 'N/A')}")
        if result.get('features'):
            print(f"   Features: {', '.join(result['features'])}")
        print(f"   URL: {result.get('url', 'N/A')}")


def main():
    """Main execution function."""
    print("="*60)
    print("SCRAPER IMMOBILIARE - MONSELICE")
    print("="*60)

    # Load configuration
    config = load_config()

    print("\nSearch criteria:")
    criteria = config['search_criteria']
    print(f"  Location: {criteria['location']}")
    print(f"  Price: €{criteria['price_min']:,} - €{criteria['price_max']:,}")
    print(f"  Area: {criteria['area_min']}-{criteria['area_max']} m²")
    print(f"  Rooms: {criteria['rooms']}")
    print(f"  Type: {criteria['property_type']}")
    print(f"  Features: {', '.join(criteria['features'])}")

    # Initialize scrapers
    scrapers = [
        ImmobiliareScraper(config),
        CasaitScraper(config),
        IdealistaScraper(config),
        SubitoScraper(config)
    ]

    # Run all scrapers and collect results
    all_results = []

    for scraper in scrapers:
        try:
            results = scraper.scrape()
            all_results.extend(results)
        except Exception as e:
            print(f"Error running {scraper.get_site_name()}: {e}")
            continue

    # Save and display results
    if all_results:
        save_results(all_results, config['output'])
        print_summary(all_results)
    else:
        print("\n" + "="*60)
        print("No matching properties found.")
        print("Try adjusting your search criteria in config.json")
        print("="*60)


if __name__ == "__main__":
    main()
