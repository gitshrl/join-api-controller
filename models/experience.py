from db import db
from datetime import datetime


class ExperienceModel(db.Model):
    __tablename__ = 'Experiences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    company = db.Column(db.String(50))
    start_date = db.Column(db.DateTime(timezone=False))
    end_date = db.Column(db.DateTime(timezone=False))
    description = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, name, company, start_date, end_date, description, 
        date_created, date_modified, user_id):
        self.name = name
        self.company = company
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.user_id = user_id

    def json(self):
        return {
            "name": self.name,
            "company": self.company,
            "start_date": self.start_date\
                .strftime("%m-%d-%Y"),
            "end_date": self.end_date\
                .strftime("%m-%d-%Y"),
            "description": self.description,
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
