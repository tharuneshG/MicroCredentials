from flask import Flask
from flask_mail import Mail

from flask_mail import Mail, Message
app1 = Flask(__name__)

app1.config['MAIL_SERVER'] = 'smtp.gmail.com'
app1.config['MAIL_PORT'] = 465
app1.config['MAIL_USERNAME'] = 'tharunesh.1502247@gmail.com'
app1.config['MAIL_DEFAULT_SENDER'] = 'tharunesh.1502247@gmail.com'
app1.config['MAIL_PASSWORD'] = 'born@June27'
app1.config['MAIL_USE_TLS'] = False
app1.config['MAIL_USE_SSL'] = True
app1.config['SECRET_KEY'] = 'tharunesh@1997'
mail = Mail(app1)
mail.init_app(app1)
