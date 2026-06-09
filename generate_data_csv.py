import csv
import json
import os

CSV_FILE_PATH = "products.csv"
JSON_OUTPUT_PATH = "data/products.json"

def convert_spreadsheet_to_json():
    # Verify the spreadsheet exists before running
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: Could not find '{CSV_FILE_PATH}' in your folder.")
        print("Please save your Excel sheet as a CSV file in this directory first.")
        return

    print(f"Reading columns from {CSV_FILE_PATH}...")
    product_list = []

    # Open the spreadsheet file with UTF-8 encoding to prevent text errors
    with open(CSV_FILE_PATH, mode="r", encoding="utf-8-sig") as csv_file:
        # DictReader automatically turns the first row into column headers
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Skip empty rows if you accidentally hit enter in Excel
            if not row.get("title"):
                continue
                
            # Clean up the whitespace around each cell value
            clean_row = {key.strip(): value.strip() for key, value in row.items()}
            product_list.append(clean_row)

    catalog_data = {"entries": product_list}

    # Ensure the Hugo data directory exists and write the JSON file
    os.makedirs(os.path.dirname(JSON_OUTPUT_PATH), exist_ok=True)
    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2, ensure_ascii=False)
        
    print(f"Spreadsheet Sync Successful: Processed {len(product_list)} items into {JSON_OUTPUT_PATH}.")

if __name__ == "__main__":
    convert_spreadsheet_to_json()