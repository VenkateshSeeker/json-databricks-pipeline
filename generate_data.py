import json
import os
import random
import uuid
from datetime import datetime, timedelta

OUTPUT_PATH = "data/output.json"

PRODUCTS = ["Milk", "Bread", "Rice", "TV", "Laptop", "Phone", None]
CATEGORIES = ["Grocery", "Electronics", "Home", None]
PAYMENT_METHODS = ["CARD", "UPI", "CASH", "NETBANKING", None]

def random_timestamp():
    return (
        datetime.utcnow()
        - timedelta(minutes=random.randint(0, 10000))
    ).isoformat()

def generate_record(i):
    record = {
        "transaction_id": str(uuid.uuid4()) if random.random() > 0.05 else None,
        "store_id": random.randint(100, 110),
        "product": random.choice(PRODUCTS),
        "category": random.choice(CATEGORIES),
        "quantity": random.choice([1, 2, 3, None, "two"]),
        "price": random.choice([49.99, 199.99, None, "N/A"]),
        "currency": "INR",
        "payment": {
            "method": random.choice(PAYMENT_METHODS),
            "success": random.choice([True, False, "true", 1])
        },
        "customer": {
            "customer_id": random.choice([random.randint(1000, 2000), None]),
            "loyalty_member": random.choice([True, False, None])
        },
        "event_time": random_timestamp(),
        "ingestion_time": datetime.utcnow().isoformat()
    }

    # Schema drift: sometimes add a new column
    if random.random() > 0.85:
        record["discount_applied"] = random.choice([5, 10, None])

    # Unexpected junk field
    if random.random() > 0.9:
        record["extra_info"] = {"note": "manual override"}

    return record

def main():
    os.makedirs("data", exist_ok=True)

    records = [generate_record(i) for i in range(200)]

    with open(OUTPUT_PATH, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(f"Generated {len(records)} records")

if __name__ == "__main__":
    main()
