import json
import os
from bs4 import BeautifulSoup
# Replace traditional requests with curl_cffi browser impersonator
from curl_cffi import requests

SHOP_URL = "https://www.etsy.com/shop/wearadare"

def fetch_live_listings():
    print(f"Connecting to live shop via impersonated browser: {SHOP_URL}...")
    
    # impersonate="chrome" mimics Chrome's exact TLS fingerprint signature
    response = requests.get(SHOP_URL, impersonate="chrome")
    
    if response.status_code != 200:
        print(f"Error fetching page: Status {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Targeted Etsy grid element selectors
    cards = soup.select(".js-merch-stash-hovercard-rows .responsive-listing-grid-item")
    if not cards:
        cards = soup.select("div[data-listing-id]")

    products = []
    for card in cards:
        try:
            title_element = card.select_one("h3") or card.select_one(".listing-title") or card.select_one(".v2-listing-card__title")
            title = title_element.text.strip() if title_element else "Premium Design"

            link_element = card.select_one("a")
            etsy_link = link_element["href"].split("?")[0] if link_element else SHOP_URL

            price_element = card.select_one(".currency-value")
            price = price_element.text.strip() if price_element else "0.00"

            img_element = card.select_one("img")
            image_url = img_element.get("src") or img_element.get("data-src")
            
            # Clean thumbnail tags to ensure high-res cover files load instead
            if image_url and "il_340x270" in image_url:
                image_url = image_url.replace("il_340x270", "il_570xN")

            products.append({
                "title": title,
                "price": price,
                "image_url": image_url,
                "etsy_share_link": etsy_link
            })
        except Exception:
            continue

    return {"entries": products}

if __name__ == "__main__":
    catalog = fetch_live_listings()
    
    if catalog and catalog["entries"]:
        os.makedirs("data", exist_ok=True)
        with open("data/products.json", "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"Success! Captured {len(catalog['entries'])} live listings from your store.")
    else:
        print("Failed to pull elements. Check if layout patterns shifted.")