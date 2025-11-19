from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://nyaganya:password123@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()