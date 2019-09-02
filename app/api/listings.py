from app.analysis.analysis_helper import get_daily_counts
from app.api import bp
from app.models import Listing
from app.api.errors import bad_request
from app.api.auth import token_auth
from app import db
from flask import jsonify, request, url_for, g, abort


@bp.route('/listings', methods=['GET'])
@token_auth.login_required
def get_listings():
    page = min(request.args.get('page', 1, type=int), 10) # Limit page and page number to privatize data
    per_page = min(request.args.get('per_page', 10, type=int), 20)
    data = Listing.to_collection_dict(Listing.query, page, per_page, 'api.get_listings')
    return jsonify(data)


@bp.route('/listings/<int:id>', methods=['GET'])
@token_auth.login_required
def get_listing(id):
    return jsonify(Listing.query.get_or_404(id).to_dict())


@bp.route('/fields', methods=['GET'])
def get_fields():
	with open('app/notifications/field_dict.txt') as f:
		body = f.read()
	return body


@bp.route('/listings/get_course_counts', methods=['GET', 'POST'])
def get_course_counts():
    daily_counts = get_daily_counts()
    return daily_counts
