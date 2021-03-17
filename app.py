import os

from db import db
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from flask_cors import CORS, cross_origin

from resources.user import (
    User, 
    UserRegister, 
    UserLogin, 
    UserUpdate, 
    UserList, 
    UserLogout, 
    AvatarUpload
)
from resources.skill import Skill, SkillRegister
from resources.experience import Experience, ExperienceRegister
from resources.license import License, LicenseRegister
from resources.portfolio import Portfolio, PortfolioRegister
from resources.project import (
    Project, 
    ProjectList, 
    ProjectRegister,
    UserProjectList, 
    ThumbnailUpload
)
from resources.collaborator import Collaborator, CollaboratorRegister
from resources.joined_project import (
    JoinedProject, 
    JoinedProjectRegister, 
    JoinedProjectList
)
from resources.comment import Comment, CommentRegister, ProjectCommentList
from resources.reply import Reply, ReplyRegister
from resources.chat import ChatRegister, UserChatList
from resources.role import Role, RoleRegister
from resources.report import Report, ReportRegister


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_SECRET_KEY'] = "j01n-pr0j3ct"
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['CORS_HEADERS'] = 'Content-Type'

jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins" : "*"}})

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(User, "/user/<int:id>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserUpdate, "/user/update/<int:id>")
api.add_resource(AvatarUpload, "/avatar/upload/<int:id>")

api.add_resource(Skill, "/skill/<int:id>")
api.add_resource(SkillRegister, "/skill/register")

api.add_resource(Experience, "/experience/<int:id>")
api.add_resource(ExperienceRegister, "/experience/register")

api.add_resource(License, "/license/<int:id>")
api.add_resource(LicenseRegister, "/license/register")

api.add_resource(Portfolio, "/portfolio/<int:id>")
api.add_resource(PortfolioRegister, "/portfolio/register")

api.add_resource(Project, "/project/<int:id>")
api.add_resource(ProjectList, "/projects")
api.add_resource(ProjectRegister, "/project/register")
api.add_resource(UserProjectList, "/project/<int:user_id>")
api.add_resource(ThumbnailUpload, "/thumbnail/upload/<int:id>")
api.add_resource(UserLogout, '/user/logout')

api.add_resource(Collaborator, "/collaborator/<int:id>")
api.add_resource(CollaboratorRegister, "/collaborator/register")

api.add_resource(JoinedProject, "/joined_project/<int:id>")
api.add_resource(JoinedProjectRegister, "/joined_project/register")
api.add_resource(JoinedProjectList, "/joined_projects")

api.add_resource(Comment, "/comment/<int:id>")
api.add_resource(CommentRegister, "/comment/register")
api.add_resource(ProjectCommentList, "/comment/project/<int:project_id>")

api.add_resource(Reply, "/reply/<int:id>")
api.add_resource(ReplyRegister, "/reply/register")

api.add_resource(ChatRegister, "/chat/register")
api.add_resource(UserChatList, "/chat/recipent/<int:recipent_id>")

api.add_resource(Role, "/role/<int:id>")
api.add_resource(RoleRegister, "/role/register")

api.add_resource(Report, "/report/<int:id>")
api.add_resource(ReportRegister, "/report/register")

db.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
