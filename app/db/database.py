import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# host = os.getenv("DB_HOST")
# port = os.getenv("DB_PORT")
# database = os.getenv("DB_NAME")
# user = os.getenv("DB_USER")
# password = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL =os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()