import requests
from flask import current_app

def create_applicant(payload):
    print(payload)
    base_url = current_app.config['SUMSUB_API_URL']
    level_name = payload.get('levelName', 'basic-kyc-level')  # Default to 'basic-kyc-level' if not provided
    endpoint = f'/resources/applicants?levelName={level_name}'
    url = f"{base_url}{endpoint}"   
    print(url, 'url')

    headers = {
        "content-type": "application/json",
        "X-App-Token": current_app.config['SUMSUB_API_TOKEN'],
    }
    print(headers, 'headers')   
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
