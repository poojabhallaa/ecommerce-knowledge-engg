# Products Knowledge — Restaurants & Menus

QuickBite's catalog is organized as **Restaurants → Menu Categories → Items**.

## Restaurant Model

Each restaurant has:

- `restaurant_id` — unique identifier
- `name`, `cuisine` (e.g., Italian, Indian, Fast Food)
- `rating` — average customer rating (1–5)
- `avg_prep_time_minutes` — average kitchen preparation time
- `is_open` — whether the restaurant is currently accepting orders
- `min_order_value` — minimum cart value required to place an order
- `delivery_radius_km` — maximum distance served from the restaurant

## Menu Item Model

Each menu item has:

- `item_id`, `restaurant_id`, `name`, `category` (e.g., Starters, Main Course, Dessert, Beverages)
- `price`
- `is_veg` — vegetarian flag
- `is_available` — whether the item is currently in stock
- `customizations` — optional add-ons (e.g., extra cheese, spice level)

## Catalog Rules

- Items marked `is_available: false` cannot be added to a cart.
- A restaurant that is `is_open: false` cannot receive new orders, even if its
  items are individually marked available.
- Prices are stored exclusive of tax; tax is applied at checkout per
  `rules/business_rules.json`.
- Restaurants can run item-level or cart-level promotions (see `policies.md`
  for how discounts interact with delivery fees).

## Sample Catalog Snapshot

See `data/sample_data.json` for structured records. As of the last sync, the
sample data includes:

- **Restaurants**: Pasta Palace (Italian), Spice Route (Indian), Burger Barn (Fast Food)
- **Categories**: Starters, Main Course, Dessert, Beverages
- Each restaurant has 3–5 sample menu items with prices and availability flags
