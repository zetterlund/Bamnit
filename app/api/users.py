from app.api import bp
from app.models import User, Notification
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth
from app import db
from flask import jsonify, request, url_for, g, abort


@bp.route('/me', methods=['GET', 'PUT', 'DELETE'])
@token_auth.login_required
def me():
    if request.method == 'GET':
        data = g.current_user.to_dict(include_email=True)
        return jsonify(data)
    if request.method == 'PUT':
        user = User.query.get_or_404(g.current_user.id)
        data = request.get_json() or {}
        if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
            return bad_request('please use a different username')
        if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
            return bad_request('please use a different email address')
        if data.get('notifications_enabled', None) not in [True, False, None]:
            return bad_request('please use only true/false for "notifications_enabled" field')
        user.from_dict(data, new_user=False)
        db.session.commit()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user = User.query.filter_by(id=g.current_user.id).first()
        db.session.delete(user)
        db.session.commit()
        response = jsonify({})
        response.status_code = 200
        return response


@bp.route('/me', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email, and password')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
# @token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>/notifications', methods=['GET', 'POST'])
@token_auth.login_required
def get_notifications(id):
    if g.current_user.id != id:
        return error_response(401, 'You may only view/edit your own notifications')
    if request.method == 'GET':
        user = User.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = Notification.to_collection_dict(user.notifications, page, per_page, 'api.get_notifications', id=id)
        return jsonify(data)
    if request.method == 'POST':
        data = request.get_json() or {}
        n = Notification()
        setattr(n, "user_id", id)
        n.from_dict(data, new_notification=True)
        db.session.add(n)
        db.session.commit()
        response = jsonify(n.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_notification', user_id=id, notification_id=n.id)
        return response


@bp.route('/users/<int:user_id>/notifications/<int:notification_id>', methods=['GET', 'PUT', 'DELETE'])
@token_auth.login_required
def get_notification(user_id, notification_id):
    if g.current_user.id != user_id:
        return error_response(401, 'You may only view/edit your own notifications')
    n = Notification.query.get_or_404(notification_id)
    if request.method == 'GET':
        return jsonify(n.to_dict())
    if request.method == 'PUT':
        data = request.get_json() or {}
        n.from_dict(data)
        db.session.commit()
        return jsonify(n.to_dict())
    if request.method == 'DELETE':
        db.session.delete(n)
        db.session.commit()
        response = jsonify({})
        response.status_code = 200
        return response