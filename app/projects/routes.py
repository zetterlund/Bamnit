from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.projects import bp
from app.projects.riotgames import MatchPredictor

from flask import session
# from .forms import LoginForm


# Home page for 'Projects' section
@bp.route('/index.html', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def projects():
    return render_template('projects/projects.html', title='Projects', heading='Projects')


@bp.route('/chained-words', methods=['GET', 'POST'])
def chained_words():
    return render_template('projects/chained_words.html', title='Chained Words', heading='Chained Words')


@bp.route('/riot', methods=['GET', 'POST'])
def match_predictor():
    return render_template('projects/riot_match_predictor.html', title='ARAM Match Predictor', heading='ARAM Match Predictor')


@bp.route('/riot/get_prediction', methods=['GET', 'POST'])
def get_prediction():
    champion_list = request.form
    results = MatchPredictor().make_prediction(champion_list)
    return jsonify(results)
