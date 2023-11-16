# user_application.py
from . import db
from datetime import datetime

# user_application.py
class UserApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wf_app_id = db.Column(db.Integer)
    protocol = db.Column(db.Enum('http', 'https'), default='http')
    ip_ver = db.Column(db.Enum('ipv4', 'ipv6'), default='ipv4')
    ip_addr = db.Column(db.String(40), default='0.0.0.0')
    port = db.Column(db.Integer, default=80)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    # UserApplication 모델과 User 모델 간의 관계 (다대일)
    user = db.relationship('User', backref=db.backref('user_applications', lazy=True))

    @classmethod
    def create(cls, **kwargs):
        application = cls(**kwargs)
        db.session.add(application)
        db.session.commit()
        return application
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
