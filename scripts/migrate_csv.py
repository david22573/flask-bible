import csv
from pathlib import Path

from app.db import SessionLocal, engine
from app.models import Base, Book, Chapter, Verse

BOOKS_CSV = Path("data/books.csv")
CHAPTERS_CSV = Path("data/chapters.csv")
VERSES_CSV = Path("data/verses.csv")


def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


def load_books():
    with BOOKS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        books = [
            Book(
                id=int(row["id"]),
                name=row["name"],
                testament=row["testament"],
                book_order=int(row["book_order"]),
                total_chapters=int(row["total_chapters"]),
            )
            for row in reader
        ]
    return books


def load_chapters():
    with CHAPTERS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        chapters = [
            Chapter(
                id=int(row["id"]),
                book_id=int(row["book_id"]),
                chapter_number=int(row["chapter_number"]),
                total_verses=int(row["total_verses"]),
            )
            for row in reader
        ]
    return chapters


def load_verses():
    with VERSES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        verses = [
            Verse(
                id=int(row["id"]),
                book_id=int(row["book_id"]),
                chapter_number=int(row["chapter_number"]),
                verse_number=int(row["verse_number"]),
                text=row["text"],
            )
            for row in reader
        ]
    return verses


def migrate():
    """Run full migration."""
    init_db()

    with SessionLocal() as db:
        print("Inserting books...")
        db.bulk_save_objects(load_books())
        db.commit()

        print("Inserting chapters...")
        db.bulk_save_objects(load_chapters())
        db.commit()

        print("Inserting verses...")
        # Insert in batches if CSV is large
        BATCH_SIZE = 1000
        verses = load_verses()
        for i in range(0, len(verses), BATCH_SIZE):
            db.bulk_save_objects(verses[i : i + BATCH_SIZE])
            db.commit()

    print("Migration completed!")


if __name__ == "__main__":
    migrate()
