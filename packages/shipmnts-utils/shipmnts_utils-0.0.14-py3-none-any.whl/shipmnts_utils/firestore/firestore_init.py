from google.cloud import firestore


class Firestore:
    def __init__(self):
        self.fs_client = firestore.Client()
