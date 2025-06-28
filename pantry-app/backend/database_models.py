class User:
    def __init__(self, id, username, email, hashed_password, refresh_token):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.refresh_token = refresh_token

class PantryItem:
    def __init__(self, id, name, quantity, category, expiration_date, user_id):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.category = category
        self.expiration_date = expiration_date
        self.user_id = user_id