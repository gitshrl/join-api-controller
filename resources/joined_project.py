from datetime import datetime
from flask_restful import Resource, reqparse

from models.joined_project import JoinedProjectModel


class JoinedProject(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
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
        'thumbnail',
        type=str,
        required=False      
    )
    parser.add_argument(
        'status',
        type=int,
        required=False
    )

    def delete(self, id):
        joined_project = JoinedProjectModel.find_by_id(id)

        if joined_project:
            joined_project.delete_from_db()
            return {'message': 'Joined project deleted'}, 201
        
        return {'message': 'Project not found.'}, 404

    def put(self, id):
        data = JoinedProject.parser.parse_args()

        joined_project = JoinedProjectModel.find_by_id(id)

        if data['name'] is not None:
            joined_project.name = data['name']
        if data['description'] is not None:
            joined_project.description = data['description']
        if data['due_date'] is not None:
            joined_project.due_date = data['due_date']
        if data['num_req_collaborator'] is not None:
            joined_project.num_req_collaborator = data['num_req_collaborator']
        if data['thumbnail'] is not None:
            joined_project.thumbnail = data['thumbnail']
        if data['status'] is not None:
            joined_project.status = data['status']

        try:
            joined_project.save_to_db()
        except:
            return {"message": "An error occurred updating the joined project."}, 500

        return joined_project.json(), 201


class JoinedProjectRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
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
        'thumbnail',
        type=str,
        required=False
    )
    parser.add_argument(
        'status',
        type=int,
        required=False
    )
    parser.add_argument(
        'project_1_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'project_2_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )

    def post(self):
        data = JoinedProjectRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()
        data['thumbnail'] = 'default_thumbnail.jpg'
        data['status'] = 0

        joined_project = JoinedProjectModel(**data)

        joined_project.save_to_db()

        try:
            joined_project.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the joined project."
            }, 500

        return joined_project.json(), 201


class JoinedProjectList(Resource):
    def get(self):
        return [x.json() for x in JoinedProjectModel.query.all()]
