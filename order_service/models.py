
class Order:
    def __init__(self, user_id, product_name, price , quantity):
        self.user_id = user_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity":self.quantity
        }
