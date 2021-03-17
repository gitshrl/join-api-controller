from datetime import datetime
from flask_restful import Resource, reqparse

from models.report import ReportModel


class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'comment',
        type=str,
        required=False
    )

    def delete(self, id):
        report = ReportModel.find_by_id(id)

        if report:
            report.delete_from_db()
            return {'message': 'Report deleted'}, 201
        
        return {'message': 'Report not found.'}, 404

    def put(self, id):
        data = Report.parser.parse_args()

        report = ReportModel.find_by_id(id)

        if data['type'] is not None:
            report.type = data['type']
        if data['comment'] is not None:
            report.comment = data['comment']

        try:
            report.save_to_db()
        except:
            return {"message": "An error occurred updating the report."}, 500
        
        return report.json(), 201


class ReportRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'comment',
        type=str,
        required=False
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'project_id',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    def post(self):
        data = ReportRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        report = ReportModel(**data)

        try:
            report.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the report."
            }, 500
        
        return report.json(), 201
