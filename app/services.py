# app/services.py

import requests
from flask import current_app

class SumsubDocument:
    @staticmethod
    def add_document(applicant_id, file_path):
        base_url = current_app.config['SUMSUB_API_URL']
        endpoint = f'/resources/applicantActions/{applicant_id}/images'
        url = f"{base_url}{endpoint}"

        headers = {
            "X-App-Token": current_app.config.get('SUMSUB_API_TOKEN'),
            "Content-Type": "multipart/form-data"
        }

        files = {
            'content': (file_path, open(file_path, 'rb'), 'application/octet-stream')
        }

        response = requests.post(url, headers=headers, files=files)
        return response.json()
