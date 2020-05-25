from flask import Blueprint, render_template
from flask_login import login_required, current_user



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', selected='index')

@main.route('/profile')
@login_required
def profile():
    print('go to profile')
    return render_template('profile.html', name=current_user.name)