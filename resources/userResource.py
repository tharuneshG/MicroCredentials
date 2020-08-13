import random
import sqlite3
from datetime import date
from random import randint

from flask_mail import Message, Mail
from flask_restful import Resource, reqparse

from mail import mail, app1
from models.user import UserModel

today = date.today()
mail = Mail(app1)

class UserRegister(Resource):
    TABLE_NAME = 'user'

    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('contact_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('qualification',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('salary',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pan_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type_of_employer',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('name_of_employer',
                        type=str,
                        required=True,
                        )

    # Method to generate user_id
    def userid(self, data):
        income = int(data['salary'])
        salary_per_year = income * 12
        if int(salary_per_year) <= 500000:
            user_type_id = 'A'
        elif int(salary_per_year) > 500000 & int(salary_per_year) <= 1000000:
            user_type_id = 'B'
        elif int(salary_per_year) > 1000000 & int(salary_per_year) <= 1500000:
            user_type_id = 'C'
        elif int(salary_per_year) > 1500000 & int(salary_per_year) <= 3000000:
            user_type_id = 'D'
        elif int(salary_per_year) > 3000000:
            user_type_id = 'E'

        get_list = UserList.get(self)
        user_list = get_list['users']
        if len(user_list) == 0:
            num = 0
        else:
            for iterator in user_list:
                usrid = iterator['user_id']
                if user_type_id == (usrid.split('-')[0]):
                    latestid = (usrid.split('-')[1])
                else:
                    latestid ="-1"
            num = int(latestid) + 1
        user_id = user_type_id + '-' + str(num)
        return user_id

    # Method to generate password
    def password(self, data):
        date = today.strftime("%d")
        month = today.strftime("%b")
        random_number = randint(100, 999)
        character = random.choice('$_')
        password = str(date) + str(month) + str(character) + str(random_number)
        return password

    # Email Generation
    def emailgeneration(self, data, user_id, password):
        msg = Message('Dear User,', sender='tharunesh.1502247@gmail.com', recipients=[data['email']])
        msg.body = "Your user id is " + user_id + " and your password is " + password
        mail.send(msg)

    # post method
    def post(self):
        data = UserRegister.parser.parse_args()
        user_id = self.userid(data)
        password = self.password(data)
        if UserModel.find_by_email(data['email']):
            return {"message": "User with that email id already exists."}, 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)".format(
            table=self.TABLE_NAME)
        cursor.execute(query, (
            data['first_name'], data['last_name'], data['date_of_birth'], data['address'], data['contact_no'],
            data['email'], data['qualification'], data['gender'], data['salary'], data['pan_no'],
            data['type_of_employer']
            , data['name_of_employer'], user_id, password))
        connection.commit()
        connection.commit()
        self.emailgeneration(
            data, user_id, password
        )
        connection.close()
        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
