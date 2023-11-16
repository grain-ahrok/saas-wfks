# domain.py
from . import db
from datetime import datetime

# domain.py
class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    user_application_id = db.Column(db.Integer, db.ForeignKey('user_application.id'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


    
    @classmethod
    def create(cls, **kwargs):
        domin = cls(**kwargs)
        db.session.add(domin)
        db.session.commit()
        return domin