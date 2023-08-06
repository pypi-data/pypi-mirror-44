import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore as fsa
from google.cloud import firestore

class Firestore:
    def __init__(self):
        self.fs_client = firestore.Client()

