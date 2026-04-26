from app.model.db.user import User
from app.utlis.logger import logger


class UserRepository:
    async def get_user(self, username: str) -> User | None:
        user = await User.find_one(User.username == username)
        logger.debug(
            "user retrived from database with username=%s, user: %s", username, user
        )
        return user

    async def save_user(self, user: User) -> User:
        saved_user = await user.insert()
        logger.debug("user saved to database, user: %s", saved_user)
        return saved_user
