from db import db
from datetime import datetime

from models.user import UserModel


class CollaboratorModel(db.Model):
    __tablename__ = 'Collaborators'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, default=0, nullable=False)
    
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project = db.relationship('ProjectModel')
    
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    def __init__(self, date_created, date_modified, status, project_id, 
        user_id):
        self.date_created = date_created
        self.date_modified = date_modified
        self.status = status
        self.project_id = project_id
        self.user_id = user_id
    
    def json(self):
        user = UserModel.find_by_id(self.user_id)
        return {
            "id": self.user_id,
            "fullname": user.fullname,
            "email": user.email,
            "phone": user.phone,
            "organization": user.organization,
            "position": user.position,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "status": self.status
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

    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query.filter_by(project_id=project_id).all()
