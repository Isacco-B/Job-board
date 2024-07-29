import os
from dotenv import load_dotenv

load_dotenv()

NODE_ENV = os.getenv("NODE_ENV")
PORT = os.getenv("PORT")

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
PASSWORD_TOKEN_SECRET = os.getenv("PASSWORD_TOKEN_SECRET")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_NAME = os.getenv("EMAIL_NAME")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_SECURITY = os.getenv("EMAIL_SECURITY")

DATABASE_URL = os.getenv("DATABASE_URL")
