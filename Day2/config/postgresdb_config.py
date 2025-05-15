from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")

DB_URL=f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}"

engine =create_engine(DB_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
