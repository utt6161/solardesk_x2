from flask import Blueprint, render_template

module = Blueprint('blog', __name__, url_prefix='/', template_folder='templates')

