import os
import time
import random
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import sys
sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def insert_random_order():
  
    with engine.begin() as conn:
        customer = conn.execute(
            text("SELECT * FROM customer ORDER BY RANDOM() LIMIT 1;")
        ).mappings().first()

        if not customer:
            print("Нет покупателей в базе.")
            return

        customer_id = customer["customer_id"]
        billing_address = customer["address"]
        billing_city = customer["city"]
        billing_state = customer["state"]
        billing_country = customer["country"]
        billing_postal = customer["postal_code"]

        invoice_date = datetime.now()
        total = 0

        result = conn.execute(text("""
    INSERT INTO invoice (
        customer_id, invoice_date, billing_address, billing_city,
        billing_state, billing_country, billing_postal_code,
        longitude, latitude, total
    )
    VALUES (
        :customer_id, :invoice_date, :billing_address, :billing_city,
        :billing_state, :billing_country, :billing_postal,
        :longitude, :latitude, :total
    )
    RETURNING invoice_id
"""), {
    "customer_id": customer_id,
    "invoice_date": invoice_date,
    "billing_address": billing_address,
    "billing_city": billing_city,
    "billing_state": billing_state,
    "billing_country": billing_country,
    "billing_postal": billing_postal,
    "longitude": customer["longitude"],
    "latitude": customer["latitude"],
    "total": total
})

        invoice_id = result.scalar()

        for _ in range(random.randint(1, 3)):
            track = conn.execute(
                text("SELECT track_id, unit_price FROM track ORDER BY RANDOM() LIMIT 1;")
            ).mappings().first()

            if not track:
                continue

            track_id, unit_price = track["track_id"], track["unit_price"]
            quantity = random.randint(1, 3)
            line_total = unit_price * quantity
            total += line_total

            conn.execute(text("""
                INSERT INTO invoice_line (invoice_id, track_id, unit_price, quantity)
                VALUES (:invoice_id, :track_id, :unit_price, :quantity)
            """), {
                "invoice_id": invoice_id,
                "track_id": track_id,
                "unit_price": unit_price,
                "quantity": quantity
            })

        conn.execute(
            text("UPDATE invoice SET total = :total WHERE invoice_id = :invoice_id"),
            {"total": round(total, 2), "invoice_id": invoice_id}
        )

        print(f"Случайная покупка #{invoice_id} (customer {customer_id}, total={total:.2f})")


if __name__ == "__main__":
    while True:
        insert_random_order()
        time.sleep(15)
