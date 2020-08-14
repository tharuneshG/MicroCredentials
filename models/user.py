from flask import Flask
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


from database import database


class UserModel(database.Model):
    __tablename__ = 'user'

    first_name = database.Column(database.String(60))
    last_name = database.Column(database.String(60))
    date_of_birth = database.Column(database.String(10))
    address = database.Column(database.String(100))
    contact_no = database.Column(database.Integer)
    email = database.Column(database.String(80))
    qualification = database.Column(database.String(80))
    gender = database.Column(database.String(80))
    salary = database.Column(database.Integer)
    pan_no = database.Column(database.String(80))
    type_of_employer = database.Column(database.String(100))
    name_of_employer = database.Column(database.String(100))
    user_id = database.Column(database.String(100), primary_key=True)
    password = database.Column(database.String(100))

    def __init__(self, first_name, last_name, date_of_birth, address, contact_no, email, qualification, gender, salary,
                 pan_no, type_of_employer, name_of_employer, user_id, password):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.contact_no = contact_no
        self.email = email
        self.qualification = qualification
        self.gender = gender
        self.salary = salary
        self.pan_no = pan_no
        self.type_of_employer = type_of_employer
        self.name_of_employer = name_of_employer
        self.user_id = user_id
        self.password = password

    def json(self):
        return {'first_name': self.first_name,
                'last_name': self.last_name,
                'date_of_birth': self.date_of_birth,
                'address': self.address,
                'contact_no': self.contact_no,
                'email': self.email,
                'qualification': self.qualification,
                'gender': self.gender,
                'salary': self.salary,
                'pan_no': self.pan_no,
                'type_of_employer': self.type_of_employer,
                'name_of_employer': self.name_of_employer,
                'user_id': self.user_id,
                'password': self.password
                }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    @classmethod
    def find_by_login(cls, user_id, password):
        return cls.query.filter_by(user_id=user_id, password=password).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_from_database(self):
        database.session.delete(self)
        database.session.commit()

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        app = Flask(__name__)
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
