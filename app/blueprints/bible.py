from flask import Blueprint, abort, jsonify, render_template

from app.db import Session
from app.models import Book, Chapter

bp = Blueprint("bible", __name__)


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def get_book_by_slug(session, slug: str):
    book = session.query(Book).filter_by(slug=slug).first()
    if not book:
        abort(404, description="Book not found")
    return book


@bp.route("/")
def home():
    with Session() as session:
        books = session.query(Book).order_by(Book.id).all()
    testaments = {"Old": [], "New": []}
    for book in books:
        testaments[book.testament].append(to_dict(book))
    return render_template("index.html", testaments=testaments)


@bp.route("/book/<string:book_slug>/")
def book_view(book_slug):
    with Session() as session:
        book_obj = get_book_by_slug(session, book_slug)
        first_chapter = (
            session.query(Chapter)
            .filter_by(book_id=book_obj.id, chapter_number=1)
            .first()
        )
        verses = [to_dict(v) for v in first_chapter.verses] if first_chapter else []
    return render_template(
        "book.html",
        book=to_dict(book_obj),
        initial_chapter=(
            {**to_dict(first_chapter), "verses": verses} if first_chapter else None
        ),
    )


@bp.route("/book/<string:book_slug>/chapter/<int:chapter_number>")
def chapter_view(book_slug, chapter_number):
    with Session() as session:
        book_obj = get_book_by_slug(session, book_slug)
        chapter = (
            session.query(Chapter)
            .filter_by(book_id=book_obj.id, chapter_number=chapter_number)
            .first()
        )
        if not chapter:
            abort(404, description="Chapter not found")
        verses = [to_dict(v) for v in chapter.verses]
    return render_template(
        "book.html",
        book=to_dict(book_obj),
        initial_chapter={**to_dict(chapter), "verses": verses},
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
        verses = [to_dict(v) for v in chapter.verses]
        return jsonify({**to_dict(chapter), "verses": verses})


@bp.route("/cube")
def cube():
    return render_template("cube.html")
