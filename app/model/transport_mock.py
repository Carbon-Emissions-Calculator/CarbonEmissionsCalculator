import uuid

# Mock database (em memória)
mock_db = []

class MockUser:
    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        mock_db.append(self)

    @classmethod
    def objects(cls):
        return mock_db

    @classmethod
    def get(cls, user_id):
        for user in mock_db:
            if user.id == user_id:
                return user
        return None

    @classmethod
    def delete(cls, user_id):
        global mock_db
        mock_db = [user for user in mock_db if user.id != user_id]
