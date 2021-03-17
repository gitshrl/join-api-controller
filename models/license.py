from db import db
from datetime import datetime

class LicenseModel(db.Model):
    __tablename__ = 'Licenses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    issue_date = db.Column(db.DateTime(timezone=False))
    exp_date = db.Column(db.DateTime(timezone=False))
    organization = db.Column(db.String(50))
    description = db.Column(db.String(255))
    credential = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, name, issue_date, exp_date, organization, description,
        credential, date_created, date_modified, user_id):
        self.name = name
        self.issue_date = issue_date
        self.exp_date = exp_date
        self.organization = organization
        self.description = description
        self.credential = credential
        self.date_created = date_created
        self.date_modified = date_modified
        self.user_id = user_id

    def json(self):
        return {
            "name": self.name,
            "issue_date": self.issue_date\
                .strftime("%m-%d-%Y"),
            "exp_date": self.exp_date\
                .strftime("%m-%d-%Y"),
            "organization": self.organization,
            "description": self.description,
            "credential": self.credential,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "user_id": self.user_id
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
   
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
