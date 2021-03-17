from db import db
from datetime import datetime

from models.user import UserModel


class ReplyModel(db.Model):
    __tablename__ = 'Replies'

    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.TEXT, nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    comment_id = db.Column(db.Integer, db.ForeignKey('Comments.id'))
    comment = db.relationship('CommentModel')

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, reply, date_created, date_modified, comment_id, 
        user_id):
        self.reply = reply
        self.date_created = date_created
        self.date_modified = date_modified
        self.comment_id = comment_id
        self.user_id = user_id
    
    def json(self):
        user = UserModel.find_by_id(self.user_id)

        return {
            "id": self.id,
            "reply": self.reply,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "comment_id": self.comment_id,
            "user": {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "avatar": user.avatar
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
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id).all()