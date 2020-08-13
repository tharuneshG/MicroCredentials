from database import database


class PolicyModel(database.Model):
    __tablename__ = 'policy_table'

    policy_name = database.Column(database.String(80))
    start_date = database.Column(database.String(80))
    end_date = database.Column(database.String(80))
    duration_in_years = database.Column(database.String(80))
    company_name = database.Column(database.String(100))
    initial_deposit = database.Column(database.Integer)
    policy_type = database.Column(database.String(80))
    user_type = database.Column(database.String(80))
    terms_per_year = database.Column(database.Integer)
    term_amount = database.Column(database.Integer)
    interest = database.Column(database.Float)
    maturity_amount = database.Column(database.Float)
    policy_id = database.Column(database.String(120), primary_key=True)

    def __init__(self, policy_name, start_date, end_date, duration_in_years, company_name, initial_deposit, policy_type,
                 user_type, terms_per_year, term_amount,
                 interest, maturity_amount, policy_id):
        self.policy_name = policy_name
        self.start_date = start_date
        self.end_date = end_date
        self.duration_in_years = duration_in_years
        self.company_name = company_name
        self.initial_deposit = initial_deposit
        self.policy_type = policy_type
        self.user_type = user_type
        self.terms_per_year = terms_per_year
        self.term_amount = term_amount
        self.interest = interest
        self.maturity_amount = maturity_amount
        self.policy_id = policy_id

    def json(self):
        return {

            'policy_name': self.policy_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'duration_in_years': self.duration_in_years,
            'company_name': self.company_name,
            'initial_deposit': self.initial_deposit,
            'policy_type': self.policy_type,
            'user_type': self.user_type,
            'terms_per_year': self.terms_per_year,
            'term_amount': self.term_amount,
            'interest': self.interest,
            'maturity_amount': self.maturity_amount,
            'policy_id': self.policy_id

        }

    @classmethod
    def find_by_policy_name(cls, policy_name):
        return cls.query.filter_by(policy_name=policy_name).first()

    @classmethod
    def find_by_company_name(cls, company_name):
        return cls.query.filter_by(company_name=company_name).first()

    @classmethod
    def find_by_policy_id(cls, policy_id):
        return cls.query.filter_by(policy_id=policy_id).first()

    @classmethod
    def find_by_policy_type(cls, policy_type):
        return cls.query.filter_by(policy_type=policy_type).get()

    @classmethod
    def find_by_years(cls, duration_in_years):
        return cls.query.filter_by(duration_in_years=duration_in_years).get()

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    def delete_to_database(self):
        database.session.delete(self)
        database.session.commit()
