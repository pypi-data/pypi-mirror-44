from google.cloud import firestore


def initialize_firestore():
    fs_client = firestore.Client()
    return fs_client
