"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
import psycopg2
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import MyForm, PhotoForm,LoginForm
from app.models import Users,Follows,Likes,Posts
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import date

# Note: that when using Flask-WTF we need to import the Form Class that we created
# in forms.py

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/basic-form', methods=['GET', 'POST'])
def basic_form():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        return render_template('result.html',firstname=firstname,lastname=lastname,email=email)
    return render_template('form.html')

def connect_db():
    return psycopg2.connect(host="localhost",database="project_two", user="postgres", password="123") 

@app.route('/register', methods=['GET', 'POST'])
def register():
    myform = MyForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            # Note the difference when retrieving form data using Flask-WTF
            # Here we use myform.firstname.data instead of request.form['firstname']
            
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
            
            cur.execute('insert into Users (username,password,firstname,lastname,email,location,biography) values (%s, %s, %s, %s, %s, %s, %s)',(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography']))
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
    
@app.route('/wtform', methods=['GET', 'POST'])
@login_required
def wtform():
    myform = MyForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            # Note the difference when retrieving form data using Flask-WTF
            # Here we use myform.firstname.data instead of request.form['firstname']
            
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
            
            cur.execute('insert into Users (username,password,firstname,lastname,email,location,biography) values (%s, %s, %s, %s, %s, %s, %s)',(request.form['username'],request.form['password'],request.form['firstname'],request.form['lastname'],request.form['email'], request.form['location'],request.form['biography']))
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
    return render_template('wtform.html', form=myform)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wtform'))

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
            return redirect(next_page or url_for('wtform'))
        else:
            flash('Username or Password is incorrect.', 'danger')

    flash_errors(form)
    return render_template('login.html', form=form)
    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))


# This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
    
@app.route('/photo-upload', methods=['GET', 'POST'])
def photo_upload():
    photoform = PhotoForm()

    if request.method == 'POST' and photoform.validate_on_submit():

        photo = photoform.photo.data # we could also use request.files['photo']
        description = photoform.description.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('display_photo.html', filename=filename, description=description)

    flash_errors(photoform)
    return render_template('photo_upload.html', form=photoform)

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
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