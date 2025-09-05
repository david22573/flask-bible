from calendar import c

from flask import Blueprint, ctx, render_template

from app.db import Session
from app.models import Book, Chapter

bp = Blueprint("bible", __name__)


@bp.route("/")
def home():
    with Session() as session:
        books = session.query(Book).all()
    testaments = {"Old": [], "New": []}
    for book in books:
        if book.testament == "Old":
            testaments["Old"].append(book)
        else:
            testaments["New"].append(book)
    ctx = {"testaments": testaments}
    return render_template("index.html", **ctx)


@bp.route("/book/<int:book_id>")
def book(book_id):
    with Session() as session:
        book = session.get(Book, book_id)
    return render_template("book.html", book=book)


@bp.route("/chapter/<int:chapter_id>")
def chapter(chapter_id):
    with Session() as session:
        chapter = session.get(Chapter, chapter_id)
        if not chapter:
            return "Chapter not found", 404
        ctx = {"chapter": chapter, "verses": chapter.verses}
    return render_template("chapter.html", **ctx)


@bp.route("/cube")
def cube():
    return render_template("cube.html")
