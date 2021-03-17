from db import db
from sqlalchemy import or_
from datetime import datetime

from models.project import ProjectModel


class JoinedProjectModel(db.Model):
    __tablename__ = 'JoinedProjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    due_date = db.Column(db.DateTime(timezone=False))
    num_req_collaborator = db.Column(db.Integer, default=0, nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    thumbnail = db.Column(db.String(50))
    status = db.Column(db.Integer, default=0, nullable=False)
    
    project_1_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project_1 = db.relationship('ProjectModel', foreign_keys=[project_1_id])

    project_2_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project_2 = db.relationship('ProjectModel', foreign_keys=[project_2_id])

    def __init__(self, name, description, due_date, num_req_collaborator,
        date_created, date_modified, thumbnail, status, project_1_id, project_2_id):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.num_req_collaborator = num_req_collaborator
        self.date_created = date_created
        self.date_modified = date_modified
        self.thumbnail = thumbnail
        self.status = status
        self.project_1_id = project_1_id
        self.project_2_id = project_2_id

    def json(self):
        project_1 = ProjectModel.find_by_id(self.project_1_id).json()
        project_2 = ProjectModel.find_by_id(self.project_2_id).json()

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date\
                .strftime("%m-%d-%Y"),
            "num_req_collaborator": self.num_req_collaborator,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "thumbnail": self.thumbnail,
            "status": self.status,
            "project_1": {
                "id": project_1['id'],
                "name": project_1['name'],
                "type": project_1['type'],
                "owner": project_1['owner'],
                "collaborators": [p for p in project_1['collaborators']],
            },
            "project_2": {
                "id": project_2['id'],
                "name": project_2['name'],
                "type": project_2['type'],
                "owner": project_2['owner'],
                "collaborators": [p for p in project_2['collaborators']],
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
    def find_by_project_id(cls, project_id):
        conds = [
            JoinedProjectModel.project_1_id == project_id, 
            JoinedProjectModel.project_2_id == project_id
        ]
        return cls.query.filter(or_(*conds)).all()
