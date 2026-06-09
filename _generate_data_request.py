import json
import os
import requests
from bs4 import BeautifulSoup

# TARGET: Put your exact public Etsy shop URL here
SHOP_URL = "https://www.etsy.com/shop/wearadare" 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_live_listings():
    print(f"Connecting to live shop storefront: {SHOP_URL}...")
    response = requests.get(SHOP_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching page: Status {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate individual listing cards on the shop front page
    cards = soup.select(".js-merch-stash-hovercard-rows .responsive-listing-grid-item")
    
    # Fallback if Etsy layout nesting structure varies slightly
    if not cards:
        cards = soup.select("div[data-listing-id]")

    products = []
    print(f"Found {len(cards)} active listings to parse.")

    for card in cards[:6]: # Test with the first 6 items for layout validation
        try:
            # 1. Title
            title_element = card.select_one("h3") or card.select_one(".listing-title")
            title = title_element.text.strip() if title_element else "Premium Collection Item"

            # 2. Listing URL
            link_element = card.select_one("a")
            etsy_link = link_element["href"].split("?")[0] if link_element else SHOP_URL

            # 3. Price
            price_element = card.select_one(".currency-value")
            price = price_element.text.strip() if price_element else "0.00"

            # 4. Raw Image Source
            img_element = card.select_one("img")
            image_url = img_element.get("src") or img_element.get("data-src")
            
            # Clean image string to ensure high-resolution crop loading
            if image_url and "il_340x270" in image_url:
                image_url = image_url.replace("il_340x270", "il_570xN")

            products.append({
                "title": title,
                "price": price,
                "image_url": image_url,
                "etsy_share_link": etsy_link
            })
        except Exception as e:
            continue

    return {"entries": products}

if __name__ == "__main__":
    catalog = fetch_live_listings()
    
    if catalog and catalog["entries"]:
        os.makedirs("data", exist_ok=True)
        with open("data/products.json", "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"Success! Exported {len(catalog['entries'])} live products into data/products.json.")
    else:
        print("Failed to parse product array elements.")