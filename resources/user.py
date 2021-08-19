from flask_restful import Resource, reqparse

from code.models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="The username cannot be left blank"
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="The password cannot be left blank"
    )

    def post(self):
        request_data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(request_data['username'])
        if user:
            return {"message": "User already exists"}
        user = UserModel(**request_data)
        UserModel.save_user_to_db(user)

        return {"message": "User created"}, 201

