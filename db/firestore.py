import google.cloud.firestore as firestore

# Initialize Firestore client
db = firestore.Client()

def get_db():
    return db