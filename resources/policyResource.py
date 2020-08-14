import sqlite3
from datetime import datetime, timedelta

from flask_mail import Message, Mail
from flask_restful import Resource, reqparse

from mail import mail, app1
from models.policy import PolicyModel
from resources.userResource import today

mail = Mail(app1)


class PolicyRegister(Resource):
    TABLE_NAME = 'policy_table'

    parser = reqparse.RequestParser()

    parser.add_argument('policy_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('start_date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('duration_in_years',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('initial_deposit',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('policy_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('terms_per_year',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('term_amount',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('interest',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def policyid(self, data):
        """Generates and returns the policy_id"""
        if data['policy_type'] == 'Vehicle Insurance':
            policy_type_id = 'VI'
        elif data['policy_type'] == 'Travel Insurance':
            policy_type_id = 'TI'
        elif data['policy_type'] == 'Health Insurance':
            policy_type_id = 'HI'
        elif data['policy_type'] == 'Life Insurance':
            policy_type_id = 'LI'
        elif data['policy_type'] == 'Child Plans':
            policy_type_id = 'CP'
        elif data['policy_type'] == 'Retirement Plans':
            policy_type_id = 'RT'

        year_of_start_date = today.strftime("%Y")
        get_list = PolicyList.get(self)
        policy_list = get_list['policies']
        if len(policy_list) == 0:
            num = '001'
        else:
            for iterator in policy_list:
                policyid = iterator['policy_id']
                if policy_type_id == (policyid.split('-')[0]):
                    latestid = (policyid.split('-')[2])
                else:
                    latestid = "000"
            num = "{:03d}".format(int(latestid) + 1)

            datestring = data['start_date']
            dt = datetime.strptime(datestring, '%d/%m/%Y')
            year_of_start_date = dt.strftime("%Y")

        policy_id = policy_type_id + '-' + year_of_start_date + '-' + num
        return policy_id

    def maturityAmount(self, data):
        """Calculate and returns the maturity amount"""
        amount = int(data['duration_in_years']) * int(data['terms_per_year']) * int(data['term_amount'])
        interest = float(data['interest']) / 100
        maturity_amount = int(data['initial_deposit']) + amount + (amount * interest)
        return maturity_amount

    def endDate(self, data):
        """Calculate and returns the end_date"""
        start_date = datetime.strptime(data['start_date'], '%d/%m/%Y')
        duration = data['duration_in_years']
        total_days = int(duration) * 365
        end_date = (start_date + timedelta(days=total_days)).strftime("%d/%m/%Y")
        return end_date

    def emailgeneration(self, data, policy_id, end_date):
        """Sends the email to the admin"""
        msg = Message('Policy register', sender='tharunesh.1502247@gmail.com', recipients=['tharuneshevils@gmail.com'])
        msg.body = f"""Hi Admin
        The policy is successfully registered.The policy {policy_id} is available to the users from {data['start_date']}
to {end_date} """
        mail.send(msg)

    def post(self):
        """Saves the data to the databse"""
        data = PolicyRegister.parser.parse_args()
        policy_id = self.policyid(data)
        maturity_amount = self.maturityAmount(data)
        end_date = self.endDate(data)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (
        data['policy_name'], data['start_date'], end_date, data['duration_in_years'], data['company_name'],
        data['initial_deposit'], data['policy_type'], data['user_type'], data['terms_per_year'],
        data['term_amount'], data['interest'], maturity_amount, policy_id))
        connection.commit()
        self.emailgeneration(data, policy_id, end_date)
        connection.close()

        return {"message": "Policy created successfully."}, 201


class PolicyList(Resource):
    def get(self):
        """Retrieves the data from database"""
        return {'policies': list(map(lambda x: x.json(), PolicyModel.query.all()))}
