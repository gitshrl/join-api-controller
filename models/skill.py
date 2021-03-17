from db import db
from datetime import datetime

class SkillModel(db.Model):
    __tablename__ = 'Skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    familiarity = db.Column(db.Enum('1', '2', '3', '4', '5'))
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, name, familiarity, date_created, date_modified, 
        user_id):
        self.name = name
        self.familiarity = familiarity
        self.date_created = date_created
        self.date_modified = date_modified
        self.user_id = user_id

    def json(self):
        return {
            "name": self.name,
            "familiarity": self.familiarity,
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

