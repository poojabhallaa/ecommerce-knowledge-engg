# Food Delivery App - Knowledge Repository

This repository is a structured knowledge base for **QuickBite**, a food delivery
platform that connects customers, restaurants, and delivery riders. It captures
how the business operates - what it sells, how orders flow, and the rules that
govern the platform - in a form that can be read by humans and queried
programmatically.

## Structure

```
ecommerce-knowledge-repository/
│
├── README.md                  # This file
│
├── knowledge/
│   ├── products.md             # Restaurants, menus, and catalog knowledge
│   ├── orders.md                # Order lifecycle and fulfillment knowledge
│   └── policies.md              # Refunds, cancellations, and platform policies
│
├── rules/
│   └── business_rules.json      # Machine-readable business rules
│
├── data/
│   └── sample_data.json         # Sample restaurants, menu items, orders, riders
│
└── knowledge_engine.py          # Python engine to query the knowledge base
```

## Domain Overview

QuickBite operates a three-sided marketplace:

- **Customers** - browse restaurants, place orders, track delivery, pay, and
  request refunds/support.
- **Restaurants** - manage menus, accept/reject orders, and prepare food within
  a target time.
- **Riders** - accept delivery jobs, pick up food, and deliver it to customers.

## Using the Knowledge Engine

`knowledge_engine.py` loads `data/sample_data.json` and `rules/business_rules.json`
and exposes simple query functions, e.g.:

```bash
python3 knowledge_engine.py
```

This runs a demo that:
- Looks up restaurants and menu items
- Calculates order totals using business rules (delivery fee, tax, discounts)
- Validates whether an order is eligible for cancellation/refund based on policy rules

## Where to Look

| Question | Where to look |
|---|---|
| What restaurants/items exist? | `knowledge/products.md`, `data/sample_data.json` |
| How does an order move from placed to delivered? | `knowledge/orders.md` |
| What are the refund/cancellation rules? | `knowledge/policies.md`, `rules/business_rules.json` |
| How do I compute a price or check a rule programmatically? | `knowledge_engine.py` |
