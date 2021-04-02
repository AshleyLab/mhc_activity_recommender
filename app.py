from flask import Flask, render_template, request, flash, Markup, jsonify, redirect, url_for

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField,\
    FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields import *

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import create_mysql_db
from update_user import update_user_main_helper
from recommend import recomend_main_helper
from rate import rate_main_helper

import config #for mysql info

user = "testuser" #now only supports one user

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' #may be easier to go this route later
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (config.mysql_user, config.mysql_password,
                                                                 config.mysql_host, config.mysql_db)

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class UpdateUserForm(FlaskForm):
    #user = StringField('user', validators=[DataRequired(), Length(1, 20)])
    #user_pref_file = StringField('user_pref_file', validators=[DataRequired(), Length(1, 20)])
    user_fitness_level = IntegerField('user_fitness_level', validators=[DataRequired(),
                                                                       NumberRange(min=1, max=5)])
    submit = SubmitField()

class RatingForm(FlaskForm):
    rating = IntegerField('rating', validators=[DataRequired(),
                                                NumberRange(min=-1, max=1)])
    exertion = IntegerField('exertion', validators=[DataRequired(),
                                                    NumberRange(min=6, max=20)])
    submit = SubmitField()

@app.route('/')
def index():
    return render_template('index.html', userForm=UpdateUserForm())

@app.route("/init")
def init():
    create_mysql_db.main()
    flash("DB Initalized")
    return render_template('index.html')
#ALTERNATIVE - Should really convert more to SQLalchemy
#@app.before_first_request
#def before_first_request_func():
#    create_mysql_db.main()

@app.route("/pref", methods=['GET', 'POST'])
def pref():
    user_pref_file = "test_feature_sets/test_feature_ranks.tsv"
    form = UpdateUserForm()
    #TODO: Add validation
    update_user_main_helper(user, user_pref_file, form.user_fitness_level.data)
    flash("Loaded features from fetest_feature_ranks.tsv and fitness level = %d" % form.user_fitness_level.data)
    return render_template('index.html', userForm=form)

@app.route("/recommendations")
def recommendations():
    #recommendations_lifestyle = recomend_main_helper("testuser", "lifestyle", 3) # Does not run
    #recommendations_training = recomend_main_helper("testuser", "training", 3) # Did not test
    recommendations_video = recomend_main_helper("testuser", "videos", 3)
    for i, data in enumerate(recommendations_video):
        data['ratingForm']= RatingForm()
        recommendations_video[i]=data
    return render_template('recommendations.html', recommendations=recommendations_video)

@app.route("/rate/<hash>/", methods=['GET', 'POST'])
def rate(hash):
    form = RatingForm()
    if form.validate():
        rate_main_helper(user, hash, "videos", form.rating.data, form.exertion.data)
        flash("Rated video")
    else:
        flash("Problem rating video")
    return redirect(url_for('recommendations'))

if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()