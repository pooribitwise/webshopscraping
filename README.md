# E-Commerce ETL Pipeline: eBay to WooCommerce 🛒

## Overview
This repository contains a complete **Extract, Transform, Load (ETL)** pipeline written in Python. It was developed to automate the large-scale migration of regional carpet inventory data from a German eBay storefront to a standalone self-hosted WordPress/WooCommerce platform[cite: 8, 9]. 

Instead of manual data entry, this suite of scripts automates the entire migration process: gathering live URLs, validating listings, scraping complex product specifications, managing image assets locally, and generating structured CSV files ready for bulk database import.

## Pipeline Architecture & Features

### 1. Data Extraction (Scraping)
* **URL Harvester (`shop_page_url_extractor.py`):** Parses eBay.de search result pages using `BeautifulSoup`, handling pagination dynamically to extract all active product URLs[cite: 3].
* **Listing Validator (`validator.py`):** Sends HTTP requests to verify the availability of products, filtering out ended or missing listings before scraping to save bandwidth and prevent errors.
* **Deep Specification Miner (`scraper_sellerN.py`):** Extracts granular product details (e.g., Price, Dimensions, Knot Count, Material/Flor, Fringe/Kette, and Status) from individual product pages. The N represent the seller template which the regex is configured for.

### 2. Asset Management
* **Automated Downloader (`csv_images_downloader.py`):** Reads mapped image URLs from CSVs and downloads high-resolution assets locally using the `requests` library.
* **Integrity Checker (`nameseqchecker.py`):** Scans the local directory for sequential naming patterns (e.g., `F1001 (1).jpg`) to identify and report missing files in the dataset.
* **Asset Categorizer (`organizer.py`):** Reorganizes local image files into specific category folders based on predefined CSV mappings.

### 3. Data Transformation & Loading (WooCommerce Prep)
* **Keyword Merger (`mergerwords.py`):** Consolidates multiple keyword text files, ensuring unique, deduplicated entries.
* **URL Mapper (`imgurlgenerator.py`):** Translates local image filenames into production-ready web server URLs (mapping to `wp-content/uploads/`) for direct database integration.
* **Bulk Import Formatter (`keywordplacer.py`):** Appends and structures metadata using the specific delimiter required for WooCommerce CSV bulk imports.

## Tech Stack
* **Language:** Python 3.x
* **Libraries:** `BeautifulSoup4` (HTML Parsing), `urllib` & `requests` (Network Requests), `colorama` (CLI Formatting), `csv`, `re` (Regex), `shutil`

## Usage
1. Clone the repository:
```bash
git clone https://github.com/pooribitwise/webshopscraping
cd webshopscraping
```
2. Install the requirements in virtual env:
```bash
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Configure the url in `shop_page_url_extractor.py`
4. Run the scripts in the sequence:
    1. `shop_page_url_extractor.py`
    2. `scraper_sellerN.py`
    3. [Optional] `csv_images_downloader.py`
5. Import your generated csv file to woocommerce.
6. Daily check:
Run validator.py daily scheduled to check if the products are still in stock and available.
## Pro Script
Use scripts under keywords.py for your exported rankmath plugin and random seo keywords for seo bulk tagging.
## Disclaimer
> **Note:** This project is for portfolio demonstration purposes, showcasing web scraping, data transformation, and automation skills. Ensure compliance with target website Terms of Service and API guidelines when deploying scrapers.

## License
This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.