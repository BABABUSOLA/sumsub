# import hashlib
# import hmac
# import json
# import time
# import requests
# from flask import current_app, jsonify

# def sign_request(request: requests.Request) -> requests.PreparedRequest:
#     prepared_request = request.prepare()
#     now = int(time.time())
#     method = request.method.upper()
#     path_url = prepared_request.path_url
#     body = b'' if prepared_request.body is None else prepared_request.body
#     if type(body) == str:
#         body = body.encode('utf-8')
#     data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
#     signature = hmac.new(
#         current_app.config['SECRET_KEY'].encode('utf-8'),
#         data_to_sign,
#         digestmod=hashlib.sha256
#     )
#     prepared_request.headers['X-App-Token'] = current_app.config['SUMSUB_API_TOKEN']
#     prepared_request.headers['X-App-Access-Ts'] = str(now)
#     prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
#     return prepared_request

# def validate_id_doc_type(id_doc_type):
#     SUPPORTED_DOC_TYPES = current_app.config['SUPPORTED_DOC_TYPES']
#     if id_doc_type not in SUPPORTED_DOC_TYPES:
#         return jsonify({'error': f"Unsupported document type: {id_doc_type}. Supported types are: {', '.join(SUPPORTED_DOC_TYPES.keys())}"}), 400
#     return None

# def create_payload(data):
#     # Define the structure of the payload with the keys we expect
#     keys = [
#         "idDocType", "idDocSubType", "country", "firstName", "middleName", 
#         "lastName", "issuedDate", "validUntil", "number", "dob", "placeOfBirth"
#     ]

#     # Create the metadata dictionary using the keys from the data object
#     metadata = {key: value for key, value in data.items() if key in keys and value}

#     # Construct the payload
#     payload = {
#         "metadata": json.dumps(metadata),  # Convert the metadata dictionary to JSON metadata
#     }
    
#     return payload


import json
from flask import jsonify,current_app
import requests
import time
import hmac
import hashlib

def sign_request(request: requests.Request) -> requests.PreparedRequest:
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url
    body = b'' if prepared_request.body is None else prepared_request.body
    if type(body) == str:
        body = body.encode('utf-8')
    data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
    signature = hmac.new(
        current_app.config['SECRET_KEY'].encode('utf-8'),
        data_to_sign,
        digestmod=hashlib.sha256
    )
    prepared_request.headers['X-App-Token'] = current_app.config['SUMSUB_API_TOKEN']
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
    return prepared_request

def validate_id_doc_type(id_doc_type):
    SUPPORTED_DOC_TYPES = current_app.config.get('SUPPORTED_DOC_TYPES',' ')
    print(SUPPORTED_DOC_TYPES, 'SUPPORTED_DOC_TYPES')
    if id_doc_type not in SUPPORTED_DOC_TYPES:
        return jsonify({'error': f"Unsupported document type: {id_doc_type}. Supported types are: {', '.join(SUPPORTED_DOC_TYPES.keys())}"}), 400
    return None

def validate_create_applicant(data):
    required_fields = ["externalUserId", "email", "phone", "lang", "type"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400

def validate_add_document(data):
    required_fields = ["idDocType", "country"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
    print("------------", data)
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