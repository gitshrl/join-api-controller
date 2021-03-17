from datetime import datetime
from flask_restful import Resource, reqparse

from models.license import LicenseModel

import datetime as dtm


class License(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every license needs a name."
    )
    parser.add_argument(
        'issue_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'exp_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'organization',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
        type=str,
        required=False
    )
    parser.add_argument(
        'credential',
        type=str,
        required=False
    )

    def delete(self, id):
        license = LicenseModel.find_by_id(id)

        if license:
            license.delete_from_db()
            return {'message': 'license deleted.'}, 200
        
        return {'message': 'license not found.'}, 404

    def put(self, id):
        data = License.parser.parse_args()

        license = LicenseModel.find_by_id(id)
        
        if data['name'] is not None:
            license.name = data['name']
        if data['issue_date'] is not None:
            license.issue_date = data['issue_date']
        if data['exp_date'] is not None:
            license.exp_date = data['exp_date']
        if data['organization'] is not None:
            license.organization = data['organization']
        if data['description'] is not None:
            license.description = data['description']
        if data['credential'] is not None:
            license.credential = data['credential']

        try:
            license.save_to_db()
        except:
            return {"message": "An error occurred updating the license."}, 500 

        return license.json(), 201


class LicenseRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every license needs a name."
    )
    parser.add_argument(
        'issue_date',
        type=str,
        required=False, 
        default=dtm.date(1, 1, 1)
    )
    parser.add_argument(
        'exp_date',
        type=str,
        required=False,
        default=dtm.date(1, 1, 1)
    )
    parser.add_argument(
        'organization',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
        type=str,
        required=False
    )
    parser.add_argument(
        'credential',
        type=str,
        required=False
    )
    parser.add_argument(
        'user_id',
        type=str,
        required=True,
        help="Every license needs a user_id."
    )

    def post(self):
        data = LicenseRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        license = LicenseModel(**data)

        try:
            license.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the license."
            }, 500

        return license.json(), 201
