import json
from os import abort
import requests
from flask import current_app
from app.utils import create_payload, sign_request

class SumsubDocument:
    @staticmethod
    def create_applicant(payload):
        # Construct the request body and params
        external_user_id = payload.get('externalUserId', '73hdkosj3738')
        level_name = payload.get('levelName', 'basic-kyc-level')

        body = {'externalUserId': external_user_id}
        params = {'levelName': level_name}
        
        # Create the request
        request = requests.Request(
            'POST',
            current_app.config['SUMSUB_API_URL'] + '/resources/applicants',
            params=params,
            data=json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Content-Encoding': 'utf-8'
            }
        )
        
        # Sign the request
        signed_request = sign_request(request)
        
        # Send the request
        session = requests.Session()
        response = session.send(signed_request, timeout=current_app.config.get('REQUEST_TIMEOUT', 60))
        
        try:
            return response.json()

        except ValueError:
            abort(400)

    @staticmethod
    def add_document(applicant_id, file_path, data):
        base_url = current_app.config['SUMSUB_API_URL']
        endpoint = f'/resources/applicants/{applicant_id}/info/idDoc'
        url = f"{base_url}{endpoint}"
        with open(file_path, 'rb') as file:
            files = {
                'content': (file_path, file, 'application/octet-stream')
            }
            # payload = {"metadata": '{"idDocType":"PASSPORT", "country":"USA"}'}
            payload = create_payload(data)
            # Create the request
            request = requests.Request('POST', url, files=files, data=payload)
            signed_request = sign_request(request)

            # Send the request
            session = requests.Session()
            response = session.send(signed_request)
            return response.json()

    @staticmethod
    def get_status(applicant_id):
        base_url = current_app.config['SUMSUB_API_URL']
        endpoint = f'/resources/applicants/{applicant_id}/requiredIdDocsStatus'
        url = f"{base_url}{endpoint}"

        # Create the request
        request = requests.Request('GET', url)
        signed_request = sign_request(request)

        # Send the request
        session = requests.Session()
        response = session.send(signed_request)
        return response.json()
