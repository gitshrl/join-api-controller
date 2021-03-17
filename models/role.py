from db import db
from datetime import datetime


class RoleModel(db.Model):
    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project = db.relationship('ProjectModel')

    collaborator_id = db.Column(db.Integer, db.ForeignKey('Collaborators.id'))
    collaborator = db.relationship('CollaboratorModel')

    def __init__(self, name, description, date_created, date_modified,
        project_id, collaborator_id):
        self.name = name
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.project_id = project_id
        self.collaborator_id = collaborator_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "description": self.description,
            "project_id": self.project_id,
            "collaborator_id": self.collaborator_id
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
    def find_by_collaborator_id(cls, collaborator_id):
        return cls.query.filter_by(collaborator_id=collaborator_id).all()



