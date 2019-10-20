from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.riotgames import bp
from app.riotgames.riotgames import MatchPredictor


@bp.route('/index.html', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def match_predictor():
    return render_template('riotgames/match_predictor.html', title='Riot Games', heading='Riot Games')



@bp.route('/get_prediction', methods=['GET', 'POST'])
def get_prediction():
    champion_list = request.form
    results = MatchPredictor().make_prediction(champion_list)

    # results = {
    #     'winningTeam': '100',
    #     'confidence': '0.58'
    # }

    return jsonify(results)
