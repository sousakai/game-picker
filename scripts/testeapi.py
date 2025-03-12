from dotenv import load_dotenv
import os

load_dotenv() 

STEAM_API_KEY = os.getenv('steam_api_key')
print(STEAM_API_KEY)  
