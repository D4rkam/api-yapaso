import firebase_admin
from firebase_admin import credentials, storage
import os

path = os.path.join(os.path.dirname(__file__), '.serviceAccountKey.json')

cred = credentials.Certificate(path)
firebase_admin.initialize_app(
    cred, {"storageBucket": "ya-paso-api.appspot.com"})

bucket = storage.bucket()
