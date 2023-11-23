# domain.py
from . import db
from datetime import datetime

# domain.py
class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    user_application_id = db.Column(db.Integer, db.ForeignKey('user_application.id'), nullable=False)
    desc = db.Column(db.String(256), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


    
    @classmethod
    def create(cls, **kwargs):
        domin = cls(**kwargs)
        db.session.add(domin)
        db.session.commit()
        return domin
    
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
    
    @classmethod
    def get_domains_by_app_id(cls, app_id):
        domains = cls.query.filter_by(user_application_id = app_id).all()
        domain_list = [{
                "id" : item.id,
                "name" : item.name,
                "desc" : item.desc } for item in domains]
        return domain_list