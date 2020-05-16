# info3180-project2
NEW !!!username:postgres, password:123, database name: project_two
db.dropall() TO DROP ALL TABLES IN DATABASE

password for database: password
username: postgres
server:localhost
database: project2
//Created Database: Posts, Users, Likes, Follows

CREATE TABLE Follows (
  id SERIAL PRIMARY KEY,
  user_id SMALLINT,
  follower_id SMALLINT
);

#bytea for pictures
#serial means autoincrement..just INSERT INTO fruits(id,name) (newline) VALUES(DEFAULT,'Apple');
                          or INSERT INTO fruits(name) (newline) VALUES('Orange');
CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) not null,
  password VARCHAR(255) not null,
  firstname VARCHAR(50) not null,
  lastname VARCHAR(50) not null,
  email VARCHAR(40) not null,
  location VARCHAR(255) not null,
  biography VARCHAR(255) not null,
  profile_photo bytea,
  joined_on DATE
);

CREATE TABLE Likes (
  id SERIAL PRIMARY KEY,
  user_id SMALLINT,
  post_id SMALLINT
);

CREATE TABLE Posts (
  id SERIAL PRIMARY KEY,
  user_id SMALLINT,
  photo bytea,
  caption VARCHAR(255) not null,
  created_on DATE
);


CREATE TABLE users (
 id SERIAL PRIMARY KEY,
 name VARCHAR(255) not null,
 email VARCHAR(255) not null
);
					                                TABS
For fonts - https://www.w3.org/Style/Examples/007/fonts.en.html
Form Validators - https://wtforms.readthedocs.io/en/2.2.1/validators/
Ideal Camera - https://www.flaticon.com/free-icon/photo-camera_832656?term=camera&page=1&position=27
Ideal Camera - https://fontawesome.com/icons/camera?style=light
Color Chart - https://htmlcolorcodes.com/color-chart/
CSS Selectors Reference - https://www.w3schools.com/cssref/css_selectors.asp
Sign In Form - https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_signup_form_modal
Login and Sign Up Example - https://tympanus.net/codrops/2012/03/27/login-and-registration-form-with-html5-and-css3/
Create a Login Form - https://www.w3schools.com/howto/howto_css_login_form.asp
Login Html CSS Example - https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_login_form
Animated Login Form - https://www.youtube.com/watch?v=ZvU57lTnNgo
Postman - https://www.postman.com/
Postgres Tutorial - https://www.postgresqltutorial.com/
Flask Documentation(!) - https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
Google search - photo in postgresql database
postgres on Cloud 9 DATABASE TABLE MAKING - https://www.youtube.com/watch?v=eTKzQWdw8pE 
Altering Table in Postgresql - https://www.postgresqltutorial.com/postgresql-add-column/
Inserting an Image in Postgresql - (!)https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
          (!)https://www.quora.com/PostgreSQL-How-can-I-store-images-in-a-database-What-existing-products-makes-it-easy-for-a-user-to-upload-photos-into-a-general-database
            https://www.postgresqltutorial.com/postgresql-python/blob/
            https://stackoverflow.com/questions/54500/storing-images-in-postgresql
            https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
Getting date in Python - https://www.geeksforgeeks.org/get-current-date-using-python/
                          https://www.programiz.com/python-programming/datetime/current-datetime
Data Types PostgreSQL - https://www.postgresqltutorial.com/postgresql-data-types/              
                      
            