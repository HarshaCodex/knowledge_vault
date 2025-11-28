import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()

url = os.getenv("DATABASE_URL")
engine = create_engine(url, echo=True)
db = sessionmaker(bind=engine)