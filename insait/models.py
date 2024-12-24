"""
insait.models module
"""

from insait.database import db


class Question(db.Model):
    """Question model"""

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
