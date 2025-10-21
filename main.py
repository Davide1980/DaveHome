#!/usr/bin/env python3
"""Main script to scrape multiple real estate websites."""

import json
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from scrapers.immobiliare import ImmobiliareScraper
from scrapers.casait import CasaitScraper
from scrapers.idealista import IdealistaScraper
from scrapers.subito import SubitoScraper


def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_to_excel(df, filename, search_criteria):
    """Save results to formatted Excel file."""
    # Create Excel file
    excel_file = filename.replace('.csv', '.xlsx')

    # Rename columns to Italian for better readability
    df_excel = df.copy()
    column_names = {
        'source': 'Fonte',
        'title': 'Titolo',
        'price': 'Prezzo (€)',
        'area': 'Superficie (m²)',
        'rooms': 'Camere',
        'location': 'Località',
        'features': 'Caratteristiche',
        'url': 'Link',
        'description': 'Descrizione'
    }
    df_excel.rename(columns=column_names, inplace=True)

    # Format features as comma-separated string
    if 'Caratteristiche' in df_excel.columns:
        df_excel['Caratteristiche'] = df_excel['Caratteristiche'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else ''
        )

    # Write to Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_excel.to_excel(writer, sheet_name='Annunci', index=False)

    # Load workbook for formatting
    wb = load_workbook(excel_file)
    ws = wb['Annunci']

    # Define styles
    header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True, size=12)

    # Price colors
    price_min = search_criteria['price_min']
    price_max = search_criteria['price_max']
    price_range = price_max - price_min

    green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
    yellow_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
    red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')

    border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    # Format header row
    for col_num, column in enumerate(df_excel.columns, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    # Format data cells
    for row_num in range(2, len(df_excel) + 2):
        for col_num, column in enumerate(df_excel.columns, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.border = border
            cell.alignment = Alignment(vertical='top', wrap_text=True)

            # Format price column with colors
            if column == 'Prezzo (€)' and cell.value:
                try:
                    price_val = float(cell.value)
                    cell.number_format = '€#,##0'

                    # Color based on price range
                    if price_val <= price_min + (price_range * 0.33):
                        cell.fill = green_fill  # Low price - good deal
                    elif price_val <= price_min + (price_range * 0.66):
                        cell.fill = yellow_fill  # Medium price
                    else:
                        cell.fill = red_fill  # High price
                except (ValueError, TypeError):
                    pass

            # Format area column
            elif column == 'Superficie (m²)' and cell.value:
                cell.number_format = '#,##0'

            # Make URLs clickable
            elif column == 'Link' and cell.value:
                cell.hyperlink = cell.value
                cell.font = Font(color='0563C1', underline='single')
                cell.alignment = Alignment(horizontal='left')

    # Auto-adjust column widths
    column_widths = {
        'Fonte': 15,
        'Titolo': 50,
        'Prezzo (€)': 15,
        'Superficie (m²)': 15,
        'Camere': 10,
        'Località': 20,
        'Caratteristiche': 25,
        'Link': 15,
        'Descrizione': 40
    }

    for col_num, column in enumerate(df_excel.columns, 1):
        col_letter = get_column_letter(col_num)
        ws.column_dimensions[col_letter].width = column_widths.get(column, 15)

    # Freeze header row
    ws.freeze_panes = 'A2'

    # Add auto-filter
    ws.auto_filter.ref = ws.dimensions

    # Set row heights
    ws.row_dimensions[1].height = 30
    for row_num in range(2, len(df_excel) + 2):
        ws.row_dimensions[row_num].height = 60

    # Save workbook
    wb.save(excel_file)

    return excel_file


def save_results(all_results, output_config, search_criteria):
    """Save results to CSV and Excel files."""
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
    csv_filename = output_config['filename'].replace('.csv', f'_{timestamp}.csv')

    # Save CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

    # Save Excel with formatting
    excel_filename = save_to_excel(df, csv_filename, search_criteria)

    print(f"\n{'='*60}")
    print(f"Results saved to:")
    print(f"  - CSV:   {csv_filename}")
    print(f"  - Excel: {excel_filename}")
    print(f"{'='*60}")

    return excel_filename


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
        save_results(all_results, config['output'], config['search_criteria'])
        print_summary(all_results)
    else:
        print("\n" + "="*60)
        print("No matching properties found.")
        print("Try adjusting your search criteria in config.json")
        print("="*60)


if __name__ == "__main__":
    main()
