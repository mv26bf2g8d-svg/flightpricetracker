import json
import os
import requests
import smtplib
from email.message import EmailMessage

API_KEY = os.environ["SEARCHAPI_KEY"]

TARGET_PRICE = 800

url = "https://www.searchapi.io/api/v1/search"

params = {
    "engine": "google_flights",
    "flight_type": "round_trip",
    "departure_id": "DFW",
    "arrival_id": "HNL",
    "outbound_date": "2027-06-07",
    "return_date": "2027-06-11",
    "included_airlines": "AA",
    "api_key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

best_price = None

if "best_flights" in data:
    prices = [f["price"] for f in data["best_flights"] if "price" in f]
    if prices:
        best_price = min(prices)

print(f"Current price: ${best_price}")

if best_price and best_price <= TARGET_PRICE:

    msg = EmailMessage()
    msg["Subject"] = f"Hawaii Flight Alert - ${best_price}"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]

    msg.set_content(
        f"DFW → HNL on American Airlines is now ${best_price} round trip."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ["EMAIL_FROM"],
            os.environ["EMAIL_PASSWORD"]
        )
        smtp.send_message(msg)

with open("prices.json", "w") as f:
    json.dump(
        {
            "last_checked_price": best_price
        },
        f,
        indent=2
    )
