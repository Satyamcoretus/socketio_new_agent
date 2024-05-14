import os
from dotenv import load_dotenv

def load_env_credentials(key:str):
    load_dotenv()
    return os.getenv(key)
