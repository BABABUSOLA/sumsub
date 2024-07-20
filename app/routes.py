from flask import Blueprint
from app.controllers import create_applicant, add_document, get_status

routes = Blueprint('routes', __name__)

@routes.route('/create_applicant', methods=['POST'])
def create_applicant_route():
    return create_applicant()

@routes.route('/add_document', methods=['POST'])
def add_document_route():
    return add_document()

@routes.route('/get_status/<applicant_id>', methods=['GET'])
def get_status_route(applicant_id):
    return get_status(applicant_id)
