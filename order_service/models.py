

class Order:
    def __init__(self, username, product_name, price , quantity):
        self.username = username
        self.product_name = product_name
        self.price = price
        self.quantity = quantity


    def to_dict(self):
        return {
            "username": self.username,
            "product_name": self.product_name,
            "price": self.price,
            "quantity":self.quantity,
        }
