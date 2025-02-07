import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Set configuration variables from .env file."""
    NICKNAME = os.getenv('NICKNAME')
    SERVER_PASS = os.getenv('SERVER_PASS')