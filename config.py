import os

class Config:
    # General Configurations
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FIRESTORE_KEY_PATH = 'serviceAccount.json'
    SUPPORTED_DOC_TYPES = {
    "ID_CARD": "An ID card.",
    "PASSPORT": "A passport.",
    "DRIVERS": "A driving license.",
    "RESIDENCE_PERMIT": "Residence permit or registration document in the foreign city/country.",
    "UTILITY_BILL": "Proof of address document.",
    "SELFIE": "A selfie with a document.",
    "VIDEO_SELFIE": "A selfie video (can be used in WebSDK and MobileSDK).",
    "PROFILE_IMAGE": "A profile image, i.e. avatar (in this case, no additional metadata should be sent).",
    "ID_DOC_PHOTO": "Photo from an ID document like a photo from the passport (In this case, no additional metadata should be sent).",
    "AGREEMENT": "An agreement, e.g. for processing personal information.",
    "CONTRACT": "A contract.",
    "DRIVERS_TRANSLATION": "Translation of the driving license required in the target country.",
    "INVESTOR_DOC": "A document from an investor, e.g. documents which disclose assets of the investor.",
    "VEHICLE_REGISTRATION_CERTIFICATE": "Certificate of vehicle registration.",
    "INCOME_SOURCE": "A proof of income.",
    "PAYMENT_METHOD": "Entity confirming payment (like bank card, crypto wallet, etc).",
    "BANK_CARD": "A bank card, like Visa or Maestro.",
    "COVID_VACCINATION_FORM": "COVID vaccination document (may contain the QR code).",
    "OTHER": "Should be used only when nothing else applies."
}

    # API Configuration
    SUMSUB_API_URL = os.environ.get('SUMSUB_API_URL') 
    SUMSUB_API_TOKEN = os.environ.get('SUMSUB_API_TOKEN')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
