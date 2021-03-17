from datetime import datetime
from flask_restful import Resource, reqparse

from models.role import RoleModel


class Role(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    def delete(self, id):
        role = RoleModel.find_by_id(id)

        if role:
            role.delete_from_db()
            return {'message': 'Role deleted'}, 201
        
        return {'message': 'Role not found.'}, 404

    def put(self, id):
        data = Role.parser.parse_args()

        role = RoleModel.find_by_id(id)

        if data['name'] is not None:
            role.name = data['name']
        if data['description'] is not None:
            role.description = data['description']
        
        try:
            role.save_to_db()
        except:
            return {"message": "An error occurred updating the role."}, 500
        
        return role.json(), 201


class RoleRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'project_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'collaborator_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )

    def post(self):
        data = RoleRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        role = RoleModel(**data)

        try:
            role.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the role."
            }, 500
        
        return role.json(), 201