from db import db
from datetime import datetime

from models.skill import SkillModel
from models.experience import ExperienceModel
from models.license import LicenseModel
from models.portfolio import PortfolioModel


class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    username = db.Column(db.String(15), nullable=False, unique=True)
    phone = db.Column(db.String(15), unique=True)
    address = db.Column(db.String(255))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime(timezone=False), 
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    avatar = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    organization = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, fullname, username, phone, address, email, password,
        date_created, date_modified, avatar, status, organization, position):
        self.fullname = fullname
        self.username = username.lower()
        self.phone = phone
        self.address = address
        self.email = email.lower()
        self.password = password
        self.date_created = date_created
        self.date_modified = date_modified
        self.avatar = avatar
        self.status = status
        self.organization = organization
        self.position = position
    
    def json(self):
        from models.project import ProjectModel
        from models.collaborator import CollaboratorModel

        _skill = SkillModel.find_by_user_id(self.id)
        _experience = ExperienceModel.find_by_user_id(self.id)
        _license = LicenseModel.find_by_user_id(self.id)
        _portfolio = PortfolioModel.find_by_user_id(self.id)
        _project = ProjectModel.find_by_user_id(self.id)
        _collaborator = CollaboratorModel.find_by_user_id(self.id)

        return {
            "id": self.id,
            "fullname": self.fullname,
            "username": self.username,
            "phone": self.phone,
            "address": self.address,
            "email": self.email,
            "password": self.password,
            "date_created": self.date_created\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "date_modified": self.date_modified\
                .strftime("%m-%d-%Y, %H:%M:%S.%f"),
            "avatar": self.avatar,
            "status": self.status,
            "organization": self.organization,
            "position": self.position,
            "num_connections": 0,
            "num_projects": len(_project) + len(_collaborator),
            "profiles": {
                "skills": [s.json() for s in _skill if _skill is not None],
                "licences": [l.json() for l in _license if _license is not None],
                "expriences": [e.json() for e in _experience if _experience is not None],
                "portfolios": [p.json() for p in _portfolio if _portfolio is not None]
            }
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
