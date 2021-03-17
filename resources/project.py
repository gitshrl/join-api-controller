import werkzeug
import os
import datetime as dtm

from datetime import datetime
from flask_restful import Resource, reqparse

from models.project import ProjectModel


class Project(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every project needs a name."        
    )
    parser.add_argument(
        'description',
        type=str,
        default='',
        required=False      
    )
    parser.add_argument(
        'type',
        type=str,
        default='',
        required=False      
    )
    parser.add_argument(
        'due_date',
        type=str,
        default=dtm.date(1, 1, 1),
        required=False      
    )
    parser.add_argument(
        'num_req_collaborator',
        type=int,
        default=0,
        required=False      
    )
    parser.add_argument(
        'thumbnail',
        type=str,
        default='thumbnail.jpg',
        required=False      
    )
    parser.add_argument(
        'status',
        type=int,
        default=0,
        required=False
    )

    def get(self, id):
        project = ProjectModel.find_by_id(id)

        if project:
            return project.json()
        
        return {
            "message": "Project not found!"
        }, 404

    def delete(self, id):
        project = ProjectModel.find_by_id(id)

        if project:
            project.delete_from_db()
            return {'message': 'Project deleted'}, 201

        return {'message': 'Project not found.'}, 404

    def put(self, id):
        data = Project.parser.parse_args()

        project = ProjectModel.find_by_id(id)

        if data['name'] is not None:
            project.name = data['name']
        if data['description'] is not None:
            project.description = data['description']
        if data['type'] is not None:
            project.type = data['type']
        if data['due_date'] is not None:
            project.due_date = data['due_date']
        if data['num_req_collaborator'] is not None:
            project.num_req_collaborator = data['num_req_collaborator']
        if data['thumbnail'] is not None:
            project.thumbnail = data['thumbnail']
        if data['status'] is not None:
            project.status = data['status']

        try:
            project.save_to_db()
        except:
            return {"message": "An error occurred updating the project."}, 500

        return project.json(), 201


class ProjectRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every project needs a name."        
    )
    parser.add_argument(
        'description',
        type=str,
        required=False      
    )
    parser.add_argument(
        'type',
        type=str,
        required=False      
    )
    parser.add_argument(
        'due_date',
        type=str,
        required=False      
    )
    parser.add_argument(
        'num_req_collaborator',
        type=int,
        required=False      
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=False      
    )

    def post(self):
        data = ProjectRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()
        data['thumbnail'] = 'default_thumbnail.jpg'
        data['status'] = 0
        
        project = ProjectModel(**data)

        try:
            project.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the project."
            }, 500

        return project.json(), 201


class ThumbnailUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'thumbnail',
        type=werkzeug.datastructures.FileStorage,
        required=True,
        location='files',
        help='This field cannot be blank.')

    def put(self, id):
        data = ThumbnailUpload.parser.parse_args()

        project = ProjectModel.find_by_id(id)

        if not project:
            return {
                "message": "Project not found!"
            }, 404

        try:
            filename = str(project.id) + '.jpg'
            data['thumbnail'].save(os.path.join('static/thumbnail', filename))

            project.thumbnail = filename
            project.save_to_db()
            
            return {
                "message": f"Project with id {project.id} updated successfully."
            }, 201
        except:
            return {"message": "An error occurred updating the thumbnail."}, 500


class ProjectList(Resource):
    def get(self):
        return [x.json() for x in ProjectModel.query.all()]


class UserProjectList(Resource):
    def get(self, user_id):
        project = ProjectModel.find_by_user_id(user_id)
        return [x.json() for x in project if project is not None]
