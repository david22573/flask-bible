import csv
from datetime import datetime
from pathlib import Path

from app.db import Session, engine
from app.models import Base, Book, Chapter, Verse

CSV_DIR = "assets/bible/kjv/csv"
BOOKS_CSV = Path(f"{CSV_DIR}/books.csv")
CHAPTERS_CSV = Path(f"{CSV_DIR}/chapters.csv")
VERSES_CSV = Path(f"{CSV_DIR}/verses.csv")


def parse_datetime(s: str) -> datetime:
    """Parse ISO datetime string, strip extra quotes, handle Zulu."""
    s_clean = s.replace('"', "")
    return datetime.fromisoformat(s_clean.replace("Z", "+00:00"))


def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


def load_books():
    with BOOKS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            Book(
                id=int(row["id"]),
                name=row["name"],
                testament=row["testament"],
                book_order=int(row["book_order"]),
                total_chapters=int(row["total_chapters"]),
                created_at=parse_datetime(row["created_at"]),
                slug=row["name"].lower().replace(" ", "-"),
            )
            for row in reader
        ]


def load_chapters():
    with CHAPTERS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            Chapter(
                id=int(row["id"]),
                book_id=int(row["book_id"]),
                chapter_number=int(row["chapter_number"]),
                total_verses=int(row["total_verses"]),
                scraped_at=parse_datetime(row["scraped_at"]),
            )
            for row in reader
        ]


def load_verses(chapter_map: dict[int, int]):
    """chapter_map: chapter_id -> book_id"""
    with VERSES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        verses = []
        for row in reader:
            chapter_id = int(row["chapter_id"])
            verses.append(
                Verse(
                    id=int(row["id"]),
                    chapter_id=chapter_id,
                    book_id=chapter_map[chapter_id],  # denormalized
                    verse_number=int(row["verse_number"]),
                    text=row["text"],
                    created_at=parse_datetime(row["created_at"]),
                )
            )
        return verses


def migrate():
    """Run full migration."""
    init_db()

    with Session() as db:
        # Insert books
        print("Inserting books...")
        db.bulk_save_objects(load_books())
        db.commit()

        # Insert chapters
        print("Inserting chapters...")
        chapters = load_chapters()
        db.bulk_save_objects(chapters)
        db.commit()

        # Build chapter_id -> book_id map for denormalized verses
        chapter_map = {c.id: c.book_id for c in chapters}

        # Insert verses in batches
        print("Inserting verses...")
        BATCH_SIZE = 1000
        verses = load_verses(chapter_map)
        for i in range(0, len(verses), BATCH_SIZE):
            db.bulk_save_objects(verses[i : i + BATCH_SIZE])
            db.commit()

    print("Migration completed!")


if __name__ == "__main__":
    migrate()
