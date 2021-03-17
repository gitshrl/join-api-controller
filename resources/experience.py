from datetime import datetime
from flask_restful import Resource, reqparse

from models.experience import ExperienceModel


class Experience(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=False,
        help="Every experience needs a name."
    )
    parser.add_argument(
        'company',
        type=str,
        required=False
    )
    parser.add_argument(
        'start_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'end_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
        type=str,
        required=False
    )

    def delete(self, id):
        experience = ExperienceModel.find_by_id(id)

        if experience:
            experience.delete_from_db()
            return {'message': 'Experience deleted.'}, 200
        
        return {'message': 'Experience not found.'}, 404

    def put(self, id):
        data = Experience.parser.parse_args()

        experience = ExperienceModel.find_by_id(id)
        
        if data['name'] is not None:
            experience.name = data['name']
        if data['company'] is not None:
            experience.company = data['company']
        if data['start_date'] is not None:
            experience.start_date = data['start_date']
        if data['end_date'] is not None:
            experience.end_date = data['end_date']
        if data['description'] is not None:
            experience.description = data['description']
 
        try:
            experience.save_to_db()
        except:
            return {"message": "An error occurred updating the experience."}, 500

        return experience.json(), 201


class ExperienceRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every experience needs a name."
    )
    parser.add_argument(
        'company',
        type=str,
        required=False
    )
    parser.add_argument(
        'start_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'end_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'description',
        type=str,
        required=False
    )
    parser.add_argument(
        'user_id',
        type=str,
        required=True,
        help="Every experience needs a profile_id."
    )

    def post(self):
        data = ExperienceRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()
        
        experience = ExperienceModel(**data)

        try:
            experience.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the experience."
            }, 500

        return experience.json(), 201
