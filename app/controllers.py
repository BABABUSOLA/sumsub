from flask import request, jsonify, abort
from app.services import SumsubDocument
from app.utils import validate_id_doc_type

def create_applicant():
    if request.method != 'POST':
        abort(405)
    
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    required_fields = ["externalUserId", "email", "phone", "lang", "type"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400

    result = SumsubDocument.create_applicant(data)
    return jsonify(result)

def add_document():
    if request.method != 'POST':
        abort(405)
    
    data = request.form
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    if not data or not file:
        return jsonify({"error": "Invalid input"}), 400
    
    required_fields = ["idDocType", "country"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400

    validate_response = validate_id_doc_type(data.get("idDocType"))
    if validate_response:
        return validate_response

    applicant_id = data.get('applicant_id')
    if not applicant_id:
        return jsonify({"error": "No applicant_id provided"}), 400

    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    response = SumsubDocument.add_document(applicant_id, file_path, data)
    return jsonify(response)

def get_status(applicant_id):
    response = SumsubDocument.get_status(applicant_id)
    return jsonify(response)
