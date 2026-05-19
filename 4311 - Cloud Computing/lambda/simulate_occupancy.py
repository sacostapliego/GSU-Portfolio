"""
AWS Lambda function to simulate real-time parking occupancy changes. Scheduled via CloudWatch Events to run every 5 minutes.
"""

import os
import random
from datetime import datetime

import psycopg2


def get_connection():
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/smart_parking",
    )
    return psycopg2.connect(database_url)


def lambda_handler(event=None, context=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, slot_count, occupied_count FROM parking_lots")
    lots = cur.fetchall()

    updated = 0
    for lot_id, name, slot_count, occupied_count in lots:
        change = random.randint(-3, 5)
        new_occupied = max(0, min(slot_count, occupied_count + change))

        if new_occupied != occupied_count:
            cur.execute(
                "UPDATE parking_lots SET occupied_count = %s, last_updated = %s WHERE id = %s",
                (new_occupied, datetime.utcnow(), lot_id),
            )
            updated += 1
            print(f"  {name}: {occupied_count} -> {new_occupied} / {slot_count}")

    conn.commit()
    cur.close()
    conn.close()

    msg = f"Updated {updated}/{len(lots)} parking lots"
    print(msg)
    return {"statusCode": 200, "body": msg}


if __name__ == "__main__":
    print("Running occupancy simulation locally...")
    result = lambda_handler()
    print(result)
