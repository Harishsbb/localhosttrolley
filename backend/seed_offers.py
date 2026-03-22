from pymongo import MongoClient

def seed_mock_offers():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['barcodedb']
    
    # Clean existing offers first (optional, but keep it clean)
    db.offers.delete_many({})
    
    offers = [
        {
            "title": "Flash Offer! 🔥",
            "product_name": "Ariel Matic Liquid Detergent 3.2 Ltr",
            "discount_label": "50% OFF",
            "tagline": "Tap to add to cart!",
            "color": "#ef4444",
            "offer_type": "pct",
            "offer_value": 50.0,
            "image": "/static/images/placeholder.svg"
        },
        {
            "title": "Sweet Deal! 🍪",
            "product_name": "Oreo Cadbury Chocolately Flavour crme Sandwich Biscuit, 288.75 Gram",
            "discount_label": "50% OFF",
            "tagline": "Guilt-free snacking!",
            "color": "#3b82f6",
            "offer_type": "pct",
            "offer_value": 50.0,
            "image": "/static/images/placeholder.svg"
        },
        {
            "title": "Summer Punch! 🥭",
            "product_name": "Maaza juice",
            "discount_label": "30% OFF",
            "tagline": "Refreshing mango magic!",
            "color": "#f59e0b",
            "offer_type": "pct",
            "offer_value": 30.0,
            "image": "/static/images/placeholder.svg"
        },
        {
            "title": "Mega Savings! ✨",
            "product_name": "Surf Excel Detergent Powder - 5kg",
            "discount_label": "₹100 OFF",
            "tagline": "Dirt is good when it's cheap!",
            "color": "#10b981",
            "offer_type": "flat",
            "offer_value": 100.0,
            "image": "/static/images/placeholder.svg"
        },
        {
            "title": "Party Pack! 🍟",
            "product_name": "Lays Chips",
            "discount_label": "BOGO Deal",
            "tagline": "Grab 'em before they're gone!",
            "color": "#8b5cf6",
            "offer_type": "pct",
            "offer_value": 100.0, # 100% off for second if free? Or just 100% value
            "image": "/static/images/placeholder.svg"
        }
    ]
    
    # Use regex to find product images for better matching (accents, cases, etc.)
    import re
    
    for offer in offers:
        # Search for a product name that matches the offer name (flexible)
        # We'll escape special chars and replace spaces with any number of spaces/chars
        escaped_name = re.escape(offer['product_name']).replace(r'\ ', '.*')
        prod = db.products.find_one({"product_name": {"$regex": f"^{escaped_name}", "$options": "i"}})
        
        if not prod:
            # Fallback search by just the first few words if no exact match
            first_word = offer['product_name'].split(',')[0].split(' ')[0]
            prod = db.products.find_one({"product_name": {"$regex": f"{first_word}", "$options": "i"}})

        if prod and prod.get('image'):
            # Convert any relative paths to consistent /static/...
            img_path = prod['image']
            if img_path.startswith('static/'):
                img_path = '/' + img_path
            offer['image'] = img_path
        else:
            offer['image'] = f"https://placehold.co/400x400/f1f5f9/94a3b8.png?text={offer['product_name'][:15]}"

    result = db.offers.insert_many(offers)
    print(f"Successfully seeded {len(result.inserted_ids)} offers.")

if __name__ == "__main__":
    seed_mock_offers()
