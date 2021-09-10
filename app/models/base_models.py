from app import db

class TimeStampedModel(db.Model):
    """
    Base model for all items
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=db.func.now(),
                           onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
