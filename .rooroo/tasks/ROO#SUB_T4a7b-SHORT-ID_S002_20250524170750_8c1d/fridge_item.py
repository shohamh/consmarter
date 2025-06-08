import datetime

class FridgeItem:
    def __init__(self, id: str, name: str, quantity: int, unit: str, expiration_date: datetime.date | None, category: str):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.expiration_date = expiration_date
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "category": self.category,
        }