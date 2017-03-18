from flask import render_template, Blueprint, request
from app.forms import *
import os
import getpass

blueprint = Blueprint('pages', __name__)


################
#### routes ####
################

@blueprint.route('/all_dirs')
def get_all_dirs():
	desktop_path = '/home/'+ getpass.getuser() +'/Desktop'
	dirs = [d for d in os.listdir(desktop_path) if os.path.isdir(os.path.join(desktop_path, d))]
	return render_template('pages/all_dirs.html', all_dirs = dirs, desktop_path = desktop_path)

@blueprint.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
