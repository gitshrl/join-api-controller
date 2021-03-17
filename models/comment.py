from db import db
from datetime import datetime

from models.user import UserModel
from models.reply import ReplyModel


class CommentModel(db.Model):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.TEXT, nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project = db.relationship('ProjectModel')

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, comment, date_created, date_modified, project_id, 
        user_id):
        self.comment = comment
        self.date_created = date_created
        self.date_modified = date_modified
        self.project_id = project_id
        self.user_id = user_id
    
    def json(self):
        user = UserModel.find_by_id(self.user_id)
        reply = ReplyModel.find_by_comment_id(self.id)
        
        return {
            "id": self.id,
            "comment": self.comment,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "project_id": self.project_id,
            "user_id": {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "avatar": user.avatar
            },
            "replies": [x.json() for x in reply if reply is not None]
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
    def find_by_project_id(cls, project_id):
        return cls.query.filter_by(project_id=project_id).all()
   
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()