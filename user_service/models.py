class User:
    def __init__(self, name, email, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
