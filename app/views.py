"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
import psycopg2
import psycopg2.extensions
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import MyForm, PhotoForm,LoginForm
from app.models import Users,Follows,Likes,Posts
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import date

# Using JWT
import jwt
from flask import _request_ctx_stack
from functools import wraps
import base64
import os

# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, 'some-secret')

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


"""@app.route('/demo')
def demo():
    # This loads a static HTML file where we then hand over the interaction
    # to VueJS
    return app.send_static_file('partials/index.html')-->"""

"""REGISTER PAGE RELATED"""
def connect_db():
    return psycopg2.connect(host="localhost",database="project_two", user="postgres", password="123") 

@app.route('/register', methods=['GET', 'POST'])
def register():
    myform = MyForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            username = myform.username.data
            password = myform.password.data
            firstname = myform.firstname.data
            lastname = myform.lastname.data
            email = myform.email.data
            location = myform.location.data
            biography = myform.biography.data
            photo = myform.photo.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            db = connect_db()
            cur = db.cursor()
            joined_on=date.today()
            
            cur.execute('insert into Users (username,password,firstname,lastname,email,location,biography,joined_on) values (%s, %s, %s, %s, %s, %s, %s,%s)',(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography'],joined_on))
            #cur.execute('insert into Users (username,password,firstname,lastname,email,location,biography,photo) values (%s,%s, %s, %s, %s, %s, %s, %s, %s)',(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography'],request.form['photo']))
            db.commit()

            flash('You have successfully filled out the form', 'success')
            #SAVING DATA TO DATABASE WITH SQLALCHEMY BELOW
            
            #user = Users(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography'],request.form['photo'],joined_on)
            user = Users(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography'],joined_on)
            db.session.add(user)
            db.session.commit()
            return render_template('result.html', username=username, password=password, firstname=firstname, lastname=lastname, email=email,
                    location=location, biography=biography,filename=filename)
        flash_errors(myform)
    return render_template('register.html', form=myform)

@app.route('/api/users/register', methods=['POST']): 
    #Accepts user information and saves it to the database
def users_register():
    myform=MyForm()
    user = [{
        "username": "myform.username.data",
        "password" = "myform.password.data",
        "firstname" = "myform.firstname.data",
        "lastname" = "myform.lastname.data",
        "email" = "myform.email.data",
        "location" = "myform.location.data",
        "biography" = "myform.biography.data",
        "photo" = "myform.photo.data"
    }]
    return jsonify(data={"user": user}, message="User successfully registered")

"""ENDING REGISTER RELATED THINGS"""
                                                                            
"""LOGIN RELATED THINGS"""
@app.route('/api/auth/login', methods=['POST']): #Accepts login credentials as username and password
def auth_login():
    user = {"username","password"}
    redirect ('generate_token')
    return jsonify(data={"user": user}, message="Success")

# This route is just used to demonstrate a JWT being generated.
@app.route('/token')
def generate_token():
    {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.XbPfbIHMI6arZ3Y922BhjWgQzWXcXNrz0ogtVhfEd2o"
    "message": "User successfully logged in."
    }
    return jsonify(error=None, data={'token': token, 'message': message})
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('basic_form'))

    form = LoginForm()
    # Login and validate the user.
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('explore'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)
"""ENDING REGISTER RELATED THINGS"""
                                                                            
"""LOGOUT RELATED THINGS"""
@app.route('/api/auth/logout', methods=['GET']): #Logout a user
@requires_auth #require token to logout
def auth_logout():
     redirect url_for('logout')
    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))
"""ENDING LOGOUT RELATED THINGS"""

"""EXPLORE PAGE RELATED THINGS"""
@app.route('/explore', methods=['GET'])
def explore():
    return render_template('explore.html')  

@app.route('/api/posts', methods=['GET']): #Return all posts for all users
@requires_auth
def posts():
    "posts": [
    {
      "id": id,
      "user_id": user_id,
      "photo": photo,
      "description": caption,
      "created_on": joined_on
    }
    ]
    return jsonify(error=None, posts=posts)
    
"""ENDING EXPLORE PAGE RELATED THINGS"""
                                                                            
"""NEW POST RELATED THINGS"""
@app.route('/api/users/{user_id}/posts', methods=['POST']): #Used for adding posts to the users feed
@requires_auth
def add_post(user_id):
    newpostform=PhotoForm()
    user{
        "id": user_id,
        "photo": ,newpostform.photo.data,
        "caption": newpostform.description.data
    }
    redirect('newpost')
    return jsonify(data={"user": user}, message="Successfully created a new post")
    
@app.route('/post/new', methods=['GET'])
def newpost():
    newpostform = PhotoForm()
    if request.method == 'POST' and newpostform.validate_on_submit():
        photo = newpostform.photo.data # we could also use request.files['photo']
        caption = newpostform.description.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('explore.html', filename=filename, caption=caption)

    flash_errors(newpostform)
    return render_template('newpost.html', form=newpostform)
 """ENDING NEW POST RELATED THINGS"""
  
@app.route('/api/users/{user_id}/posts', methods=['GET']): #Returns a user's posts
@requires_auth
def user_posts(user_id):
    #if 'id' in request.args:
    #   id = int(request.args['id'])
    #else:
    #    return "Error: No id field provided. Please provide a specific id."
    
    post = Posts.query.filter_by(user_id ='user_id')
    return render_template('explore.html', user_id=user_id)
    
@app.route('/api/users/{user_id}/follow', methods=['POST']): #Create a Follow relationship between the current user and the target user
@requires_auth
def user_follow(user_id):
    return ""
    
@app.route('/api/posts/{post_id}/like',, methods=['POST']): #Set a like on the current Post by the logged in User
@requires_auth
def posts_like(user_id):
    return ""

@app.route('/api/secure', methods=['GET'])
@requires_auth
def api_secure():
    # This data was retrieved from the payload of the JSON Web Token
    # take a look at the requires_auth decorator code to see how we decoded
    # the information from the JWT.
    user = g.current_user
    return jsonify(data={"user": user}, message="Success")


# This route doesn't require a JWT
@app.route('/api/unsecure', methods=['GET'])
def api_unsecure():
    user = {"name": "Mr. Anonymous Unsecure"}
    return jsonify(data={"user": user}, message="Success")

@app.route('/api/tasks')
@requires_auth
def tasks():
    tasks = [
        {
            'id': 1,
            'title': 'Teach class'
        },
        {
            'id': 2,
            'title': 'Give Quiz'
        },
        {
            'id': 3,
            'title': 'Do Review class for exam'
        }
    ]
    return jsonify(error=None, tasks=tasks)

# This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
    
###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
