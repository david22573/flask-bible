from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(50), unique=True, nullable=False)
    email = mapped_column(String(100), unique=True, nullable=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    testament: Mapped[str] = mapped_column(String(20), nullable=False)
    book_order: Mapped[int] = mapped_column(Integer, nullable=False)
    total_chapters: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )
    verses: Mapped[list["Verse"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    total_verses: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    scraped_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    book: Mapped["Book"] = relationship(back_populates="chapters")
    verses: Mapped[list["Verse"]] = relationship(
        back_populates="chapter", cascade="all, delete-orphan"
    )


class Verse(Base):
    __tablename__ = "verses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"), nullable=False
    )  # denormalized
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey("chapters.id"), nullable=False
    )  # proper FK
    verse_number: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    scraped_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    book: Mapped["Book"] = relationship(back_populates="verses")
    chapter: Mapped["Chapter"] = relationship(back_populates="verses")
