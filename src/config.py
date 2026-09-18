from dotenv import load_dotenv
import os

ACCESS_TOKEN_EXPIRE_SECONDS = 3600
load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY: 
    raise Exception('Не указан JWT_SECRET_KEY')