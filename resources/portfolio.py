from datetime import datetime
from flask_restful import Resource, reqparse

from models.portfolio import PortfolioModel


class Portfolio(Resource):
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
        'url',
        type=str,
        required=False
    )

    def delete(self, id):
        portfolio = PortfolioModel.find_by_id(id)

        if portfolio:
            portfolio.delete_from_db()
            return {'message': 'Portfolio deleted.'}, 200
        
        return {'message': 'Portfolio not found.'}, 404

    def put(self, id):
        data = Portfolio.parser.parse_args()

        portfolio = PortfolioModel.find_by_id(id)
        
        if data['name'] is not None:
            portfolio.name = data['name']
        if data['description'] is not None:
            portfolio.description = data['description']
        if data['start_date'] is not None:
            portfolio.start_date = data['start_date']
        if data['end_date'] is not None:
            portfolio.end_date = data['end_date']
        if data['url'] is not None:
            portfolio.url = data['url']
 
        try:
            portfolio.save_to_db()
        except:
            return {"message": "An error occurred updating the portfolio."}, 500 

        return portfolio.json(), 201


class PortfolioRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every portfolio needs a name."
    )
    parser.add_argument(
        'description',
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
        'url',
        type=str,
        required=False
    )
    parser.add_argument(
        'user_id',
        type=str,
        required=True,
        help="Every portfolio needs a user_id."
    )

    def post(self):
        data = PortfolioRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        portfolio = PortfolioModel(**data)

        portfolio.save_to_db()

        try:
            portfolio.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the portfolio."
            }, 500

        return portfolio.json(), 201