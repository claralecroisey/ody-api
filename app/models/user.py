import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __int__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return "<User %r>" % self.email

    def json(self):
        return {"id": self.id, "email": self.email}
