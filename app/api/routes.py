from flask import Blueprint, jsonify
from app.models import Player

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def test():
    return {'datadatadata': 'ooh look at this fancy data'}

@api.route('/players', methods=['GET'])
def players():
    """
    [GET] returns json data on all of the players in our database
    """
    players = [player.to_dict() for player in Player.query.all()]
    return jsonify(players)

@api.route('/player/<int:num>', methods=['GET'])
def get_number(num):
    '''
    [GET] /api/player/<int:num>
    returns all players with that number
    or None if no playes have that number
    '''
    players = Player.query.filter_by(number=num).all()
    if not players:
        return jsonify({num: None})
    return jsonify([x.to_dict() for x in players])

@api.route('/<string:tm>', methods=['GET'])
def get_team(tm):
    """
    [GET] /api/Manchester_City
    returns all players on the applicable team
    """
    tm = tm.replace('_', ' ')
    players = Player.query.filter_by(team=tm).all()
    if not players:
        return jsonify({tm: None})
    return jsonify([x.to_dict() for x in players])