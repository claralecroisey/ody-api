from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class User(db.Model):
    # The auth0 ID
    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
