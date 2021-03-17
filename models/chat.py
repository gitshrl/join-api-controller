from db import db
from datetime import datetime

from models.user import UserModel


class ChatModel(db.Model):
    __tablename__ = 'Chats'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.TEXT, nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    
    recipent_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    recipent = db.relationship('UserModel', foreign_keys=[recipent_id])

    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    sender = db.relationship('UserModel', foreign_keys=[sender_id])

    def __init__(self, message, date_created, recipent_id, sender_id):
        self.message = message
        self.date_created = date_created
        self.recipent_id = recipent_id
        self.sender_id = sender_id

    def json(self):
        recipent = UserModel.find_by_id(self.recipent_id)
        sender = UserModel.find_by_id(self.sender_id)
        
        return {
            "id": self.id,
            "message": self.message,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "recipent": {
                "id": recipent.id,
                "username": recipent.username,
                "fullname": recipent.fullname,
                "avatar": recipent.avatar
            },
            "sender": {
                "id": sender.id,
                "username": sender.username,
                "fullname": sender.fullname,
                "avatar": sender.avatar
            }
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
    def find_by_recipent_id(cls, recipent_id):
        return cls.query.filter_by(recipent_id=recipent_id).all()