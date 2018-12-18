class Admin:

    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role

    def admin_to_json(self):
        return {
            'email': self.email,
            'role': self.password
        }

    def printAdmin(self):
        print("email:%s, password:%s, role: %s" % (self.email, self.password, self.role))