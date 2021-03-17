from db import db
from datetime import datetime

from models.user import UserModel
from models.collaborator import CollaboratorModel


class ProjectModel(db.Model):
    __tablename__ = 'Projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    type = db.Column(db.String(50))
    due_date = db.Column(db.DateTime(timezone=False))
    num_req_collaborator = db.Column(db.Integer, default=0, nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    thumbnail = db.Column(db.String(50))
    status = db.Column(db.Integer, default=0, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, name, description, type, due_date, num_req_collaborator,
        date_created, date_modified, thumbnail, status, user_id):
        self.name = name
        self.description = description
        self.type = type
        self.due_date = due_date
        self.num_req_collaborator = num_req_collaborator
        self.date_created = date_created
        self.date_modified = date_modified
        self.thumbnail = thumbnail
        self.status = status
        self.user_id = user_id

    def json(self):
        user = UserModel.find_by_id(self.user_id)
        collaborator = CollaboratorModel.find_by_project_id(self.id)

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "due_date": self.due_date\
                .strftime("%m-%d-%Y"),
            "num_req_collaborator": self.num_req_collaborator,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "thumbnail": self.thumbnail,
            "status": self.status,
            "owner": {
                "id": user.id,
                "fullname": user.fullname,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "organization": user.organization,
                "position": user.position
            },
            "collaborators": [x.json() for x in collaborator if collaborator is not None]
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
