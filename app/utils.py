import json
from flask import jsonify,current_app
import requests
import time
import hmac
import hashlib

def sign_request(request: requests.Request) -> requests.PreparedRequest:
    """
    Sign a request using the secret key from the current Flask app config.

    Args:
        request (requests.Request): The request to sign.

    Returns:
        requests.PreparedRequest: The signed request.
    """
    # Prepare the request
    prepared_request = request.prepare()

    # Get the current time in seconds
    now = int(time.time())

    # Get the HTTP method of the request
    method = request.method.upper()

    # Get the path of the request
    path_url = prepared_request.path_url

    # Get the request body
    body = b'' if prepared_request.body is None else prepared_request.body

    # If the body is a string, encode it as UTF-8
    if type(body) == str:
        body = body.encode('utf-8')

    # Create the data to sign
    data_to_sign = (
        str(now).encode('utf-8')  # Current time
        + method.encode('utf-8')  # HTTP method
        + path_url.encode('utf-8')  # Request path
        + body  # Request body
    )

    # Create a new HMAC-SHA256 signature
    signature = hmac.new(
        current_app.config['SECRET_KEY'].encode('utf-8'),  # Secret key
        data_to_sign,  # Data to sign
        digestmod=hashlib.sha256  # Hash algorithm
    )

    # Add the necessary headers to the prepared request
    prepared_request.headers['X-App-Token'] = current_app.config['SUMSUB_API_TOKEN']
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()

    # Return the signed request
    return prepared_request

def validate_id_doc_type(id_doc_type):
    """
    This function validates the given `id_doc_type` by checking if it is in the list of supported document types.
    If the `id_doc_type` is not in the list, it returns a JSON response with an error message and a status code of 400.
    If the `id_doc_type` is valid, it returns `None`.

    Parameters:
    - id_doc_type (str): The document type to be validated.

    Returns:
    - None: If the `id_doc_type` is valid.
    - tuple: A tuple containing a JSON response with an error message and a status code of 400.
    """
    # Get the list of supported document types from the application configuration.
    # If the list is not defined, use an empty string as a default value.
    SUPPORTED_DOC_TYPES = current_app.config.get('SUPPORTED_DOC_TYPES',' ')
    
    # Print the list of supported document types for debugging purposes.
    print(SUPPORTED_DOC_TYPES, 'SUPPORTED_DOC_TYPES')

    # Check if the given `id_doc_type` is in the list of supported document types.
    if id_doc_type not in SUPPORTED_DOC_TYPES:
        # If the `id_doc_type` is not in the list, return a JSON response with an error message.
        # The error message includes the invalid `id_doc_type` and the list of supported document types.
        error_message = f"Unsupported document type: {id_doc_type}. Supported types are: {', '.join(SUPPORTED_DOC_TYPES.keys())}"
        return jsonify({'error': error_message}), 400
    
    # If the `id_doc_type` is valid, return `None`.
    return None

def validate_create_applicant(data):
    """
    This function validates the given `data` dictionary by checking if it contains all the required fields.
    If any of the required fields are missing, it returns a JSON response with an error message and a status code of 400.
    If all the required fields are present, it returns `None`.

    Parameters:
    - data (dict): The dictionary containing the data to be validated.

    Returns:
    - None: If all the required fields are present in the `data` dictionary.
    - tuple: A tuple containing a JSON response with an error message and a status code of 400.
    """
    # List of required fields for the data dictionary.
    required_fields = ["externalUserId", "email", "phone", "lang", "type"]
    
    # Iterate over the required fields and check if each field is present in the `data` dictionary.
    # If any required field is missing, add it to the `missing_fields` list.
    missing_fields = [field for field in required_fields if field not in data]
    
    # Check if there are any missing fields.
    if missing_fields:
        # If there are missing fields, return a JSON response with an error message indicating the missing fields.
        # The error message includes the list of missing fields.
        error_message = f"Missing required fields: {', '.join(missing_fields)}"
        return jsonify({'error': error_message, 'missing_fields': missing_fields}), 400
    
    # If all the required fields are present, return `None`.
    return None

def validate_add_document(data):
    required_fields = ["idDocType", "country"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
    validate_response = validate_id_doc_type(data.get("idDocType"))
    if validate_response:
        return validate_response
def create_payload(data):
    # Define the structure of the payload with the keys we expect
    keys = [
        "idDocType", "idDocSubType", "country", "firstName", "middleName", 
        "lastName", "issuedDate", "validUntil", "number", "dob", "placeOfBirth"
    ]

    # Create the metadata dictionary using the keys from the data object
    metadata = {key: value for key, value in data.items() if key in keys and value}

    # Construct the payload
    payload = {
        "metadata": json.dumps(metadata),  # Convert the metadata dictionary to JSON metadata
    }
    
    return payload