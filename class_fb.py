import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
try:
    cred = credentials.Certificate(json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"]))
except:
    cred = credentials.Certificate("./secrets/serviceAccountKey.json")
    
class FirebaseHandler:
    def __init__(self, cred):
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_to_attendance(self, attd_id, obj:object):
        self.db.collection("attendance").document(attd_id).set(obj)

    
#db.collection("test").document("doc").set({
#    "hello":"world"
#})