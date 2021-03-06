from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# Config Values
# location where file uploads will be stored
UPLOAD_FOLDER = './app/static/uploads'
# needed for session security, the flash() method in this case stores the message
# in a session
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zucadmulpitopj:c5e27fea902acececc52fe17d9e58c41185575295facc2e188f5792827939f86@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d7pd4rkb33pr9m'
#ORIGINAL SQLALCHEMY_DATABASE_URI: 'postgresql://postgres:123@localhost/project_two'
#postgresql://postgres:@password@localhost/project2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning
app.config['SECRET_KEY'] = '12345@idklO0L' #ORIGINAL KEY THAT EXPIRED: 'Sup3r$3cretkey'


db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # necessary to tell Flask-Login what the default route is for the login page
login_manager.login_message_category = "info"  # customize the flash message category

app.config.from_object(__name__)
from app import views

