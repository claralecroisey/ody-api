from app.models.user import User
from app import db


def create_user_if_not_exists(user_id: str):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        new_user = User(id=user_id)
        db.session.add(new_user)
        db.session.commit()
