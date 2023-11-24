# sp_ip.py
from . import db
from datetime import datetime

class SpIp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    ip_ver = db.Column(db.Enum('ipv4', 'ipv6'))
    ip_addr = db.Column(db.String(40))
    subnet_mask = db.Column(db.String(40))
    classification = db.Column(db.Enum('block', 'apply', 'exception'))
    desc = db.Column(db.String(32))
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
