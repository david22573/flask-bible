# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DuckDB file (like SQLite)
DATABASE_URL = "duckdb:///app.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
