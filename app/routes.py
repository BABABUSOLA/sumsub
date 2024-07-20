from flask import request, jsonify, abort
from app import app
from app.controllers import create_applicant
from app.services import SumsubDocument

@app.route('/create_applicant/', methods=['POST'])
def create_applicant_route():
    print('Creating applicant...')
    """
    Takes a POST request and passes the JSON data to the create_applicant
    function. Returns the response from the function as a JSON response
    object.

    :return: A JSON response object.
    """
    if request.method != 'POST':
        abort(405)
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    response = create_applicant(data)
    return jsonify(response)

@app.route('/add_document', methods=['POST'])
def add_document_route():
    """
    Endpoint for adding a document to Sumsub.

    This endpoint expects a POST request with a form data containing
    'applicant_id' and a file named 'file'. The file will be temporarily
    saved to the '/tmp' directory. The file will be uploaded to Sumsub
    using the SumsubDocument.add_document method.

    Returns a JSON response containing the response from Sumsub.

    :return: A JSON response object.
    """
    # Check if the request method is POST
    if request.method != 'POST':
        abort(405)
    
    # Get the form data and file from the request
    data = request.form
    file = request.files['file']

    # Check if the form data and file exist
    if not data or not file:
        return jsonify({"error": "Invalid input"}), 400
    
    # Get the applicant_id from the form data
    applicant_id = data.get('applicant_id')

    # Save the file temporarily to '/tmp'
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    # Upload the file to Sumsub
    response = SumsubDocument.add_document(applicant_id, file_path)

    # Return the response from Sumsub
    return jsonify(response)
