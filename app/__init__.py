from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Config Values
# location where file uploads will be stored
UPLOAD_FOLDER = './app/static/uploads'
# needed for session security, the flash() method in this case stores the message
# in a session
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/project_two'
#postgresql://postgres:@password@localhost/project2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning
app.config['SECRET_KEY'] = 'Sup3r$3cretkey'


db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # necessary to tell Flask-Login what the default route is for the login page
login_manager.login_message_category = "info"  # customize the flash message category

app.config.from_object(__name__)
from app import views