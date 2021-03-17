from datetime import datetime
from flask_restful import Resource, reqparse

from models.chat import ChatModel


class ChatRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'message',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'recipent_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'sender_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )
    
    def post(self):
        data = ChatRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()

        chat = ChatModel(**data)

        # chat.save_to_db()

        try:
            chat.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the chat."
            }, 500
        
        return chat.json(), 201


class UserChatList(Resource):
    def get(self, recipent_id):
        return [x.json() for x in ChatModel.find_by_recipent_id(recipent_id)]