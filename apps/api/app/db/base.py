from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared base of ORM models. New models are imported in app/models/__init__.py."""
