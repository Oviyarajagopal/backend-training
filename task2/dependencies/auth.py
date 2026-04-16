class FakeUser:
    def __init__(self, id):
        self.id = id

def get_current_user():
    # Temporary mock user (replace with JWT later)
    return FakeUser(id=1)