from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
MONGO_URI = 'mongodb://localhost:27017/barcodedb'
DB_NAME = 'barcodedb'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Clear existing data to avoid duplicates during testing
db.products.drop()
db.users.drop()
db.purchase_history.drop()
db.carts.drop()

print("Connected to MongoDB. Seeding data...")

# --- Products Data ---
# Data extracted from user's MySQL dump
products_data = [
    {"barcodedata": "3010000012191", "product_name": "Maaza juice", "product_price": 60.00, "quantity": 10, "image": "/static/images/2.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901491101837", "product_name": "Lays Chips", "product_price": 5.00, "quantity": 10, "image": "/static/images/1.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901063017221", "product_name": "Britannia 50-50 Maska Chaska 105g", "product_price": 28.00, "quantity": 10, "image": "/static/images/25.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901399336812", "product_name": "Softouch 2X French Perfume 2L Fabric Conditioner", "product_price": 345.00, "quantity": 10, "image": "/static/images/24.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8906014903394", "product_name": "Kwality Choco Flakes 1kg", "product_price": 229.00, "quantity": 10, "image": "/static/images/23.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901030913211", "product_name": "Boost Chocolate Nutrition Drink Powder 750g", "product_price": 450.00, "quantity": 10, "image": "/static/images/22.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "7622201703011", "product_name": "Oreo Cadbury Chocolately Flavour crème Sandwich Biscuit, 288.75 Gram", "product_price": 80.00, "quantity": 10, "image": "/static/images/21.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "4987176206695", "product_name": "Ariel Matic Liquid Detergent 3.2 Ltr", "product_price": 890.00, "quantity": 10, "image": "/static/images/20.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "7622202026621", "product_name": "Cadbury Bournvita Chocolate Nutriton Drink, 2 kg", "product_price": 780.00, "quantity": 10, "image": "/static/images/18.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8410104080204", "product_name": "Vanish 800ml", "product_price": 210.00, "quantity": 10, "image": "/static/images/17.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "6295120050040", "product_name": "Dettol Liquid Hand Wash, 675ml", "product_price": 185.00, "quantity": 10, "image": "/static/images/16.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901030602054", "product_name": "Surf Excel Detergent Powder - 5kg", "product_price": 950.00, "quantity": 10, "image": "/static/images/15.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901399111013", "product_name": "Santoor Soap (Pack of 4)", "product_price": 163.00, "quantity": 10, "image": "/static/images/14.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901088203630", "product_name": "Parachute Coconut Oil", "product_price": 126.00, "quantity": 10, "image": "/static/images/13.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "6161100950900", "product_name": "Harpic 1 Litre (pack of 2)", "product_price": 396.00, "quantity": 10, "image": "/static/images/12.jpg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901207027437", "product_name": "Dabur Honey - 1Kg", "product_price": 391.00, "quantity": 10, "image": "/static/images/10.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901287400991", "product_name": "Mysore Sandal Soap, 450g", "product_price": 232.00, "quantity": 10, "image": "/static/images/11.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "6001067021995", "product_name": "Colgate MaxFresh ToothPaste", "product_price": 72.00, "quantity": 10, "image": "/static/images/9.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901725017927", "product_name": "Sunfeast yipee family pack", "product_price": 153.00, "quantity": 10, "image": "/static/images/8.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901725132873", "product_name": "Dark fantasy choco fills", "product_price": 128.00, "quantity": 10, "image": "/static/images/7.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8906010261078", "product_name": "gold winner sunflower oil 1 L", "product_price": 190.00, "quantity": 10, "image": "/static/images/6.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8904043901015", "product_name": "Tata Salt 1kg", "product_price": 25.00, "quantity": 10, "image": "/static/images/5.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901063092716", "product_name": "Goodday Biscuit", "product_price": 10.00, "quantity": 10, "image": "/static/images/4.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "8901063164291", "product_name": "Tiger biscuit", "product_price": 10.00, "quantity": 10, "image": "/static/images/3.jpeg", "barcode_type": "EAN_13"},
    {"barcodedata": "40189384", "product_name": "Slice 1.75 L", "product_price": 95.00, "quantity": 10, "image": "/static/images/2.jpeg", "barcode_type": "EAN_8"},
    {"barcodedata": "028400199148", "product_name": "lays potato chips, classic, 8 oz", "product_price": 5.00, "quantity": 10, "image": "/static/images/1.jpeg", "barcode_type": "UPC_A"},
    {"barcodedata": "8901207046070", "product_name": "Dabur Red Toothpaste - 800g (200gx4)", "product_price": 250.00, "quantity": 10, "image": "/static/images/19.jpeg", "barcode_type": "EAN_13"}
]

db.products.insert_many(products_data)
print(f"Inserted {len(products_data)} products.")

# --- Users Data ---
# Note: User IDs are auto-generated in Mongo usually, but we can verify login by username
users_data = [
    {"username": "harish", "password": "scrypt:32768:8:1$TI81SDcdwtGQrNok$f2fed730a9776de58504c7f6dbeba28302ebda989c185246aea8496d9d0a355f907f86407f85490adadd478c721e74f96686690598463b77b3db1855c55c2f5a", "email": "harish@gmail.com", "created_at": datetime(2025, 10, 19, 14, 7, 37)},
    {"username": "lokesh", "password": "scrypt:32768:8:1$QZ6WA8Dh9yhKkTPc$92bc10d5c5b9cb7430debed3119091a1a8e2d973f4391e025f383b3b7b3fa0fe065e9a366063a0cabc53f3967f7746fee8e83850b098d4e53adf71eaa782f9e9", "email": "lokesh@gmail.com", "created_at": datetime(2025, 10, 19, 14, 10, 33)},
    {"username": "girish", "password": "scrypt:32768:8:1$ksYOqbl16lNiHkoD$001652f8f98c82e1c2e36e870884ddf3a14b48f87e8bca1962c1ae2f75845b1dd9bfcf72b596f6af13ee39889f3572a33146924ce4c304e65351d2788839d1db", "email": "girish@gmail.com", "created_at": datetime(2025, 10, 20, 8, 11, 33)},
    {"username": "sakthi", "password": "scrypt:32768:8:1$ZajJYyXbyjMrBUVN$181cfc512c9e48b175260005e1a30b89488458951654e1934618cc25c9b42328b23e424a30f8b9024194a90bb5f3f41a8cae95c6372d4676f7890cd5f3ee6c4f", "email": "sakthi@gmail.com", "created_at": datetime(2025, 10, 20, 9, 18, 36)},
    {"username": "ajith", "password": "scrypt:32768:8:1$5IwxY7GGkbP8wvWC$49718846a3f46d3def6864f9f1e784370fab549519c1ccd1e9556d3ce1f84db2a9c125a74d677d92f161a24711c096f671f0313c3898572538191b8c5b202b66", "email": "ajithkumar@gmail.com", "created_at": datetime(2025, 10, 21, 15, 16, 0)},
    {"username": "mathesh", "password": "scrypt:32768:8:1$iRtgjnLRahSTzGtg$431b06b02320c91369d137ecd557e8ccbe12125e4c0f03a46431d207cb1b1327ede6bca9caf40b58a5991f72170af5cedf6df8296f08f8312af9640fbc7c5b1c", "email": "mathesh@gmail.com", "created_at": datetime(2025, 10, 22, 20, 39, 11)},
    {"username": "harish12", "password": "scrypt:32768:8:1$EL4ybLO81Ggyc0rM$54c4fe8e734fce99ecebb8d966c8fe4c77e6e01fa001e3c78bf11d23581164011cecffbc3a07abb27ccec50c1b5ac13eb228c3d1a69628be0f33ddd935398340", "email": "harish123@gmail.com", "created_at": datetime(2025, 10, 23, 10, 28, 18)},
    {"username": "leo", "password": "scrypt:32768:8:1$eF5tYsTRpp5JvZST$ad80f9301e77de9406d2dae45522615b92938026a6cfcad5da5f443e5b9e504e31dc1856f92c5d6e0f867a41d14ead1c1f2e8314136b865dc1b1431002b3bbf6", "email": "leo@gmail.com", "created_at": datetime(2025, 10, 31, 21, 00, 48)} # Approximate time fix
]

db.users.insert_many(users_data)
print(f"Inserted {len(users_data)} users.")

print("Seeding complete!")
