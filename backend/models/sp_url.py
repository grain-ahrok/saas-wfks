# sp_url.py
from . import db
from datetime import datetime
class SpUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    url = db.Column(db.String(256))
    classification = db.Column(db.Enum('apply', 'exception'))
    desc = db.Column(db.String(32))
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
