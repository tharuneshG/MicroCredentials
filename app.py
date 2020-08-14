import sqlite3

from flask import Flask, g, jsonify, request
from flask_restful import Api
from fpdf import FPDF
from flask_httpauth import HTTPBasicAuth
from models.policy import PolicyModel
from resources.policyResource import PolicyRegister, PolicyList
from resources.userResource import UserRegister, UserList

app = Flask(__name__)
auth = HTTPBasicAuth()
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
api.add_resource(PolicyRegister, '/policyRegister')


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/policySearch", methods=["GET"])
def policy_detail_by_type():
    """Return the policy which matches the policy_id"""
    query_parameters = request.args
    policy_id = query_parameters.get('policy_id')
    print(policy_id)
    return {'policy': list(map(lambda x: x.json(), PolicyModel.query.filter_by(policy_id=policy_id)))},200


@app.route("/getDocument", methods=["GET"])
def generatepdf():
    """Generates the PDF for the given policy_id"""
    query_parameters = request.args
    policy_id = query_parameters.get('policy_id')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT policy_name from policy_table where policy_id = policy_id")
    policy_name = cursor.fetchone()
    cursor.execute("SELECT initial_deposit from policy_table where policy_id = policy_id")
    initial_deposit = cursor.fetchone()
    cursor.execute("SELECT duration_in_years  from policy_table where policy_id = policy_id")
    duration_in_years = cursor.fetchone()
    cursor.execute("SELECT interest from policy_table where policy_id = policy_id")
    interest = cursor.fetchone()
    cursor.execute("SELECT term_amount from policy_table where policy_id = policy_id")
    term_amount = cursor.fetchone()
    cursor.execute("SELECT terms_per_year from policy_table where policy_name = policy_name")
    terms_per_year = cursor.fetchone()
    cursor.execute("SELECT maturity_amount from policy_table where policy_name = policy_name")
    maturity_amount = cursor.fetchone()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=f"policy_name: {policy_name}",
             ln=1, align='L')
    pdf.cell(200, 10, txt=f"initial_deposit: {initial_deposit}",
             ln=2, align='L')
    pdf.cell(200, 10, txt=f"duration_in_year: {duration_in_years}",
             ln=2, align='L')
    pdf.cell(200, 10, txt=f"interest: {interest}",
             ln=2, align='L')
    pdf.cell(200, 10, txt=f"term_amount: {term_amount}",
             ln=2, align='L')
    pdf.cell(200, 10, txt=f"term_per_year: {terms_per_year}",
             ln=2, align='L')
    pdf.cell(200, 10, txt=f"maturity_amount: {maturity_amount}",
             ln=2, align='L')
    pdf_name = policy_id + ".pdf"
    pdf.output(pdf_name)
    return {'message': 'pdf downloaded'}, 200


api.add_resource(PolicyList, '/policyList')
api.add_resource(UserList, '/userList')


@app.route('/clearData', methods=["DELETE"])
def delete():
    """Clears the table in the database"""
    meta = database.metadata
    for table in reversed(meta.sorted_tables):
        database.session.execute(table.delete())
        database.session.commit()
    return {'message': 'data cleared'}, 200


if __name__ == '__main__':
    from database import database

    database.init_app(app)
    app.run(port=5001, debug=True)
