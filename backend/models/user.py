# user.py
from . import db,bcrypt
from datetime import datetime  # Import the datetime class from the datetime module

# user.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    membership = db.Column(db.Enum('basic', 'premium'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    # User 모델과 UserApplication 모델 간의 관계 (일대다)
    user_applications = db.relationship('UserApplication', backref='user', lazy=True)


    @classmethod
    def create(cls, **kwargs):
        hashed_password = bcrypt.generate_password_hash(kwargs['password']).decode('utf-8')
        del kwargs['password']  # Remove plain text password from kwargs
        kwargs['password'] = hashed_password
        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

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

    def change_password(self, new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
