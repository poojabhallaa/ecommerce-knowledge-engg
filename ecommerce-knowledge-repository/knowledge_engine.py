"""
Knowledge engine for the QuickBite food delivery knowledge repository.

Loads structured data (data/sample_data.json) and business rules
(rules/business_rules.json) and exposes query helpers for:
- looking up restaurants and menu items
- calculating order totals
- checking cancellation/refund eligibility
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sample_data.json")
RULES_PATH = os.path.join(BASE_DIR, "rules", "business_rules.json")


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


class KnowledgeEngine:
    def __init__(self, data_path=DATA_PATH, rules_path=RULES_PATH):
        self.data = load_json(data_path)
        self.rules = load_json(rules_path)

    # ---------- Lookups ----------

    def get_restaurant(self, restaurant_id):
        return next(
            (r for r in self.data["restaurants"] if r["restaurant_id"] == restaurant_id),
            None,
        )

    def get_menu_item(self, item_id):
        return next(
            (i for i in self.data["menu_items"] if i["item_id"] == item_id),
            None,
        )

    def get_order(self, order_id):
        return next(
            (o for o in self.data["orders"] if o["order_id"] == order_id),
            None,
        )

    def get_customer(self, customer_id):
        return next(
            (c for c in self.data["customers"] if c["customer_id"] == customer_id),
            None,
        )

    def get_menu_for_restaurant(self, restaurant_id):
        return [
            i for i in self.data["menu_items"]
            if i["restaurant_id"] == restaurant_id and i["is_available"]
        ]

    # ---------- Pricing ----------

    def find_promo(self, code):
        if not code:
            return None
        return next(
            (p for p in self.rules["promotions"]["sample_promos"] if p["code"] == code),
            None,
        )

    def calculate_order_total(self, order):
        pricing = self.rules["pricing"]

        subtotal = 0.0
        for line in order["items"]:
            item = self.get_menu_item(line["item_id"])
            if item is None:
                raise ValueError(f"Unknown item_id: {line['item_id']}")
            subtotal += item["price"] * line["quantity"]

        distance_km = order.get("distance_km", 0)
        delivery_fee = pricing["delivery"]["base_fee"] + (
            distance_km * pricing["delivery"]["per_km_rate"]
        )
        delivery_fee = min(delivery_fee, pricing["delivery"]["max_delivery_fee"])
        if subtotal >= pricing["delivery"]["free_delivery_threshold"]:
            delivery_fee = 0.0

        discount = 0.0
        promo = self.find_promo(order.get("promo_code"))
        if promo and subtotal >= promo["min_order_value"]:
            if promo["type"] == "percentage":
                discount = subtotal * (promo["value"] / 100.0)
            elif promo["type"] == "free_delivery":
                delivery_fee = 0.0

        tax = subtotal * pricing["tax_rate"]
        total = subtotal + delivery_fee + tax - discount

        return {
            "subtotal": round(subtotal, 2),
            "delivery_fee": round(delivery_fee, 2),
            "tax": round(tax, 2),
            "discount": round(discount, 2),
            "total": round(total, 2),
        }

    # ---------- Policy checks ----------

    def can_cancel(self, order):
        status = order["status"]
        policy = self.rules["cancellation_policy"]
        if status in policy["cancellable_statuses"]:
            return True, "full_refund"
        if status in policy["support_only_statuses"]:
            if status in policy["partial_refund_statuses"]:
                return True, "support_review_partial_refund"
            return True, "support_review_case_by_case"
        return False, "not_cancellable"

    def is_late_delivery(self, estimated_minutes, actual_minutes):
        grace = self.rules["order_timeouts"]["late_delivery_grace_minutes"]
        return (actual_minutes - estimated_minutes) > grace


def demo():
    engine = KnowledgeEngine()

    print("=== Restaurant Lookup ===")
    restaurant = engine.get_restaurant("R002")
    print(restaurant)

    print("\n=== Available Menu for Spice Route (R002) ===")
    for item in engine.get_menu_for_restaurant("R002"):
        print(f"- {item['name']}: ${item['price']}")

    print("\n=== Order Total Calculation (O1002) ===")
    order = engine.get_order("O1002")
    totals = engine.calculate_order_total(order)
    print(totals)

    print("\n=== Cancellation Check (O1002) ===")
    can_cancel, outcome = engine.can_cancel(order)
    print(f"Can cancel: {can_cancel}, Outcome: {outcome}")

    print("\n=== Cancellation Check (O1001 - already delivered) ===")
    delivered_order = engine.get_order("O1001")
    can_cancel, outcome = engine.can_cancel(delivered_order)
    print(f"Can cancel: {can_cancel}, Outcome: {outcome}")


if __name__ == "__main__":
    demo()
