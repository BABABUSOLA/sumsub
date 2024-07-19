from flask import request, jsonify, abort
from app import app
from app.controllers import create_applicant

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
