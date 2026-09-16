# Policies Knowledge — Cancellations, Refunds & Support

## Cancellation Policy

| Order Status at Cancellation | Who Can Cancel | Refund |
|---|---|---|
| PLACED | Customer, Restaurant, System | Full refund |
| ACCEPTED | Customer (before prep starts), Restaurant | Full refund |
| PREPARING | Restaurant or Support only | Full refund if restaurant-initiated; partial refund (cook cost deducted) if customer requests via support |
| READY_FOR_PICKUP / RIDER_ASSIGNED / PICKED_UP / OUT_FOR_DELIVERY | Support only | Case-by-case; typically no refund unless platform error |
| DELIVERED | N/A (use refund/complaint flow, not cancellation) | Not applicable |

## Refund Policy

- Refunds are issued to the original payment method within
  `refund_processing_days` (see `business_rules.json`).
- **Quality complaints** (wrong item, missing item, food quality) filed within
  `complaint_window_hours` of delivery are eligible for full or partial refund
  based on support review.
- **Late delivery**: if actual delivery time exceeds the estimated time by more
  than `late_delivery_grace_minutes`, the customer is eligible for a delivery
  fee refund or platform credit.
- Refunds for restaurant-caused cancellations (e.g., item unavailable, closed
  early) are always full refunds and do not count against the customer's
  refund history.

## Promotions & Discounts

- Only one promo code may be applied per order.
- Promo codes have a `min_order_value` and may be restricted to specific
  restaurants or customer segments (e.g., first-time users).
- Discounts apply to `subtotal` only, never to `delivery_fee` or `tax`, unless
  the promotion explicitly states "free delivery."

## Rider & Restaurant Conduct

- Restaurants that fail to accept orders within the timeout window
  (`order_accept_timeout_minutes`) beyond a set number of times in a rolling
  week may be temporarily deprioritized in search results.
- Riders are expected to maintain a minimum on-time delivery rate; repeated
  late deliveries trigger a review per internal rider policy (not covered by
  this repository).

## Support Escalation

- Support agents can override automated cancellation/refund rules for
  extenuating circumstances (e.g., accidents, natural disasters, platform
  outages), subject to manager approval for refunds above
  `manager_approval_refund_threshold`.
