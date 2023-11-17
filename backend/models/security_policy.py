# security_policy.py
from . import db
from datetime import datetime

# security_policy.py
class SecurityPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wf_security_policy_id = db.Column(db.Integer)
    request_flood = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    sql_injection = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    url_regex = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    xss = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    directory_listing = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    shellcode = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    download = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    uploadfile = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    access_control = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    evasion = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    credential_stuffing = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    cookie_protection = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    buffer_overflow = db.Column(db.Enum('exception', 'detect', 'block'), default='block')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
     # SecurityPolicy 모델과 UserApplication 모델 간의 관계 (다대일)
    applications = db.relationship('UserApplication', backref=db.backref('security_policy', lazy=True))
    urls = db.relationship('SpUrl', backref='security_policy', lazy=True)
    ips = db.relationship('SpIp', backref='security_policy', lazy=True)
    @classmethod
    def create(cls, **kwargs):
        try:
            Security_policy = cls(**kwargs)
            db.session.add(Security_policy)
            db.session.commit()
            return Security_policy
        except Exception as e:
            db.session.rollback()
            db.session.close()
            print(f"An error occurred while creating a user application: {str(e)}")
            raise  # Re-raise the exception after logging


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
    def get_domain_by_id(cls, domain_id):
        return cls.query.get(domain_id)


