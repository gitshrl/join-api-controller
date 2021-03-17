from db import db
from datetime import datetime

class ReportModel(db.Model):
    __tablename__ = 'Reports'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('Type 1', 'Type 2', 'Type 3'), nullable=False)
    comment = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=False),
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False),
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
     
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('UserModel')

    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project = db.relationship('ProjectModel')

    def __init__(self, type, comment, date_created, date_modified, 
        user_id, project_id):
        self.type = type
        self.comment = comment
        self.date_created = date_created
        self.date_modified = date_modified
        self.user_id = user_id
        self.project_id = project_id

    def json(self):
        return {
            "id": self.id,
            "type": self.type,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "user_id": self.user_id,
            "project_id": self.project_id
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
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query.filter_by(project_id=project_id).first()
