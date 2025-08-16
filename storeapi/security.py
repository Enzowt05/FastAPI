import datetime
import logging

from jose import jwt
from passlib.context import CryptContext

from storeapi.config import config
from storeapi.database import database, user_table

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM


def acess_token_expire_minutes() -> int:
    return 30


def create_acess_token(email: str):
    logger.debug("Creating acess token", extra={"email": email})
    expire = datetime.datetime.now(datetime.utc) + datetime.timedelta(
        minutes=acess_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    logging.debug("Fetching user from the database", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result
