from datetime import datetime
from flask_restful import Resource, reqparse

from models.skill import SkillModel


class Skill(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=False
    )
    parser.add_argument(
        'familiarity',
        type=str,
        required=False
    )

    
    def delete(self, id):
        skill = SkillModel.find_by_id(id)

        if skill:
            skill.delete_from_db()
            return {'message': 'Skill deleted.'}, 200
        
        return {'message': 'Skill not found.'}, 404

    def put(self, id):
        data = Skill.parser.parse_args()

        skill = SkillModel.find_by_id(id)
        
        if data['name'] is not None:
            skill.name = data['name']
        if data['familiarity'] is not None:
            skill.familiarity = data['familiarity']
        
        skill.save_to_db()

        try:
            skill.save_to_db()
        except:
            return {"message": "An error occurred updating the skill."}, 500

        return skill.json(), 201


class SkillRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every skill needs a name."
    )
    parser.add_argument(
        'familiarity',
        type=str,
        required=False
    )
    parser.add_argument(
        'user_id',
        type=str,
        required=True,
        help="Every skill needs a user_id."
    )

    def post(self):
        data = SkillRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        skill = SkillModel(**data)

        try:
            skill.save_to_db()
        except:
            return {"message": "An error occurred inserting the skill."}, 500

        return skill.json(), 201
