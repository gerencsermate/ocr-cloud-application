from beanie import Document, Indexed

class User(Document):
    username: Indexed(str, unique=True)
    password: str
    is_admin: bool = False

    class Settings:
        name = "users"
