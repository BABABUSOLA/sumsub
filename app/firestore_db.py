from google.cloud import firestore
from google.oauth2 import service_account
from config import config

def get_firestore_client():
    key_path = config['development'].FIRESTORE_KEY_PATH 
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return firestore.Client(credentials=credentials)

db = get_firestore_client()
