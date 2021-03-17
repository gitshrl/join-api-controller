from datetime import datetime
from flask_restful import Resource, reqparse

from models.reply import ReplyModel

class Reply(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'reply',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    def delete(self, id):
        reply = ReplyModel.find_by_id(id)

        if reply:
            reply.delete_from_db()
            return {'message': 'Reply deleted'}, 201

        return {'message': 'Reply not found.'}, 404

    def put(self, id):
        data = Reply.parser.parse_args()

        reply = ReplyModel.find_by_id(id)

        if data['reply'] is not None:
            reply.reply = data['reply']
        
        try:
            reply.save_to_db()
        except:
            return {"message": "An error occurred updating the reply."}, 500

        return reply.json(), 201


class ReplyRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'reply',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'comment_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )   

    def post(self):
        data = ReplyRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        reply = ReplyModel(**data)

        try:
            reply.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the reply."
            }, 500
        
        return reply.json(), 201
