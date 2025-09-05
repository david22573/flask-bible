# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DuckDB file (like SQLite)
DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

if __name__ == "__main__":
    from app.models import Base

    Base.metadata.create_all(bind=engine)
    print("Database tables created.")
