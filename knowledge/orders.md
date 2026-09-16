# Orders Knowledge — Lifecycle & Fulfillment

## Order Lifecycle

An order moves through the following states:

1. **PLACED** — Customer submits the cart; payment is authorized.
2. **ACCEPTED** — Restaurant confirms it can fulfill the order.
3. **PREPARING** — Kitchen starts cooking.
4. **READY_FOR_PICKUP** — Food is packed and waiting for a rider.
5. **RIDER_ASSIGNED** — A delivery rider is matched to the order.
6. **PICKED_UP** — Rider has collected the order from the restaurant.
7. **OUT_FOR_DELIVERY** — Rider is en route to the customer.
8. **DELIVERED** — Order handed to the customer; order is complete.
9. **CANCELLED** — Order terminated before delivery (by customer, restaurant, or system).

## Order Model

- `order_id`, `customer_id`, `restaurant_id`, `rider_id` (nullable until assigned)
- `items` — list of `{item_id, quantity, customizations}`
- `status` — one of the lifecycle states above
- `placed_at`, `delivered_at` (nullable)
- `subtotal`, `delivery_fee`, `tax`, `discount`, `total`
- `payment_method` — e.g., card, wallet, cash_on_delivery
- `delivery_address`

## Fulfillment Rules

- A restaurant has a fixed window (`order_accept_timeout_minutes` in
  `business_rules.json`) to accept or auto-reject an order.
- If no rider accepts a `READY_FOR_PICKUP` order within
  `rider_assignment_timeout_minutes`, the order is escalated to a wider rider pool.
- Estimated delivery time = restaurant `avg_prep_time_minutes` + estimated
  transit time based on distance.
- Orders can only be cancelled by the customer while in `PLACED` or `ACCEPTED`
  status (see `policies.md` for refund implications).
- Once `PICKED_UP`, an order cannot be cancelled by the customer; only support
  agents can intervene (e.g., lost order, accident).

## Order Total Calculation

```
subtotal   = sum(item.price * quantity)
delivery_fee = base_fee + (distance_km * per_km_rate)   [capped by rules]
tax        = subtotal * tax_rate
discount   = applied per active promo (see business_rules.json)
total      = subtotal + delivery_fee + tax - discount
```

This calculation is implemented in `knowledge_engine.py`.
