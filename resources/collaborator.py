from datetime import datetime
from flask_restful import Resource, reqparse

from models.collaborator import CollaboratorModel

class Collaborator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'status',
        type=int,
        required=False
    )

    def delete(self, id):
        collaborator = CollaboratorModel.find_by_id(id)

        if collaborator:
            collaborator.delete_from_db()
            return {'message': 'Collaborator deleted'}, 201
        
        return {'message': 'Collaborator not found.'}, 404
    
    def put(self, id):
        data = Collaborator.parser.parse_args()

        collaborator = CollaboratorModel.find_by_id(id)

        if data['status'] is not None:
            collaborator.status = data['status']

        try:
            collaborator.save_to_db()
        except:
            return {"message": "An error occurred updating the collaborator."}, 500

        return collaborator.json(), 201

class CollaboratorRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'project_id',
        type=int,
        required=True,
        help="Every project needs a project_id."        
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help="Every project needs a user_id."  
    )

    def post(self):
        data = CollaboratorRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()
        data['status'] = 0

        collaborator = CollaboratorModel(**data)

        try:
            collaborator.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the collaborator."
            }, 500
        
        return collaborator.json(), 201
