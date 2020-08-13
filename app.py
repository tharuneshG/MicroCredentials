from flask import Flask
from flask_restful import Api

from models.user import UserModel
from resources.userResource import UserRegister, UserList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'tharun'
api = Api(app)


@app.before_first_request
def create_tables():
    database.create_all()


api = Api(app)

api.add_resource(UserRegister, '/userRegister')
api.add_resource(UserList, '/userList')


# api.add_resource(PolicyRegister, '/policyRegister')
# api.add_resource(PolicyList, '/policyList')

@app.route('/user/<string:email>', methods=["DELETE"])
def delete(email):
    user = UserModel.find_by_email(email)
    if user:
        user.delete_from_database()
        return {'message': 'user deleted.'}
    return {'message': 'user not found.'}, 404


if __name__ == '__main__':
    from database import database

    database.init_app(app)
    app.run(port=5001, debug=True)
