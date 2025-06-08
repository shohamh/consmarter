# Inventory Core Sub-task Context (Updated)

## Goal
Implement core inventory management:
- Item CRUD operations
- Expiry tracking with custom thresholds
- Location management (fridge/pantry/freezer)
- Partial quantity expiry handling

## Dependencies
Requires project setup completion (ROO#SUB_MVP_SETUP_20250608A)

## Tech Stack
- SQLite database schema
- FastAPI endpoints
- React Native state management

## Related Files
- [Main Plan Overview](../../plans/PANTRY_APP_IMPLEMENTATION_PLAN_20250608.md)

## Constraints
- Support discrete and continuous quantities
- Handle partial consumption/expiry
- Optimize for mobile usage