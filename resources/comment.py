from datetime import datetime
from flask_restful import Resource, reqparse

from models.comment import CommentModel


class Comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'comment',
        type=str,
        required=True,
        help='This field cannot be blank.'
    )

    def delete(self, id):
        comment = CommentModel.find_by_id(id)

        if comment:
            comment.delete_from_db()
            return {'message': 'Comment deleted'}, 201

        return {'message': 'Comment not found.'}, 404

    def put(self, id):
        data = Comment.parser.parse_args()

        comment = CommentModel.find_by_id(id)

        if data['comment'] is not None:
            comment.comment = data['comment']
        
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred updating the comment."}, 500

        return comment.json(), 201

class CommentRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'comment',
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
        'user_id',
        type=int,
        required=True,
        help='This field cannot be blank.'
    )

    def post(self):
        data = CommentRegister.parser.parse_args()

        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()

        comment = CommentModel(**data)

        try:
            comment.save_to_db()
        except:
            return {
                "message": "An error occurred inserting the comment."
            }, 500
        
        return comment.json(), 201


class ProjectCommentList(Resource):
    def get(self, project_id):
        comment = CommentModel.find_by_project_id(project_id) 
        return [x.json() for x in comment if comment is not None]