# user_application.py
from . import db
from datetime import datetime

# user_application.py
class UserApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wf_app_id = db.Column(db.Integer)
    server_name = db.Column(db.Enum('enable', 'disable', default='enable'))
    status = db.Column(db.String(40))
    protocol = db.Column(db.Enum('http', 'https'), default='http')
    ip_ver = db.Column(db.Enum('ipv4', 'ipv6'), default='ipv4')
    ip_addr = db.Column(db.String(40), default='0.0.0.0')
    port = db.Column(db.Integer, default=80)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    security_policy_id = db.Column(db.Integer, db.ForeignKey('security_policy.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='user_applications', overlaps="user,user_applications")
    
    
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_domains(cls):
        return cls.query.all()
    
    @classmethod
    def get_app_by_app_id(cls, app_id) : 
        return cls.query.filter_by(id=app_id).all()
    
    @classmethod
    def get_app_by_id(cls, id) : 
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_app_by_user_id(cls, user_id) : 
        return cls.query.filter_by(user_id=user_id).all()
    

