class User:
    def __init__(self,username,  name, email, phone=None):
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "username" : self.username,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
