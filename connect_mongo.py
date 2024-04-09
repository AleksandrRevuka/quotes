import os
from dotenv import load_dotenv

from mongoengine import connect

load_dotenv()

mongo_user = os.getenv("MONGO_USER")
mongodb_pass = os.getenv("MONGO_PASSWORD")
domain = os.getenv("MONGO_DOMAIN")
db_name = os.getenv("MONGO_DB_NAME")

connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority&appName=Insight")