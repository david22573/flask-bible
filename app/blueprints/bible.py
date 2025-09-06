from flask import Blueprint, jsonify, render_template

from app.db import Session
from app.models import Book, Chapter

bp = Blueprint("bible", __name__)


def book_to_dict(book):
    return {
        "id": book.id,
        "name": book.name,
        "testament": book.testament,
        "total_chapters": book.total_chapters,
    }


def chapter_to_dict(chapter, verses):
    return {
        "id": chapter.id,
        "chapter_number": chapter.chapter_number,
        "verses": verses,
    }


def verse_to_dict(verse):
    return {
        "id": verse.id,
        "verse_number": verse.verse_number,
        "text": verse.text,
    }


@bp.route("/")
def home():
    with Session() as session:
        books = session.query(Book).order_by(Book.id).all()
    testaments = {"Old": [], "New": []}
    for book in books:
        testaments[book.testament].append(book_to_dict(book))
    return render_template("index.html", testaments=testaments)


@bp.route("/book/<int:book_id>")
def book_view(book_id):
    """Load a book page with the first chapter by default"""
    with Session() as session:
        book_obj = session.get(Book, book_id)
        if not book_obj:
            return "Book not found", 404

        first_chapter = (
            session.query(Chapter).filter_by(book_id=book_id, chapter_number=1).first()
        )

        verses = [verse_to_dict(v) for v in first_chapter.verses]
    return render_template(
        "book.html",
        book=book_to_dict(book_obj),
        initial_chapter=(
            chapter_to_dict(first_chapter, verses) if first_chapter else None
        ),
    )


@bp.route("/api/book/<int:book_id>/chapter/<int:chapter_number>")
def chapter_api(book_id, chapter_number):
    with Session() as session:
        chapter = (
            session.query(Chapter)
            .filter_by(book_id=book_id, chapter_number=chapter_number)
            .first()
        )
        if not chapter:
            return jsonify({"error": "Chapter not found"}), 404
        verses = [verse_to_dict(v) for v in chapter.verses]
        return jsonify(chapter_to_dict(chapter, verses))


@bp.route("/cube")
def cube():
    return render_template("cube.html")
