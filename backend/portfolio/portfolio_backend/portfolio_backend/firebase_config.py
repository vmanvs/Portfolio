import firebase_admin
import os
from firebase_admin import credentials, db
from useraccount.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIAL_PATH = os.path.join(BASE_DIR, 'protlogger-firebase-adminsdk-fbsvc-d6177e3c40.json')
cred = credentials.Certificate(CREDENTIAL_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://protlogger-default-rtdb.firebaseio.com/'
})

def get_db_ref(path):
    return db.reference(path)

def test_firebase_connection():
    try:
        test_ref = get_db_ref('test/connection')
        test_ref.set({'connected': True})
        result = test_ref.get()

        if result and result.get('connected') is True:
            print('Connected to Firebase')
            return True
        else:
            print('Failed to read value from connection')
            return False
    except Exception as e:
            print(f'Failed to connect to database: {str(e)}')
            return False

def set_to_database():
    ref = get_db_ref('users/testuser')
    ref.set({
        'user_id': "some_really_complicated_uuid",
        'resume_access': True,
    })

def update_database():
    ref = get_db_ref('users/testuser')
    ref.set({
        'user_id': "some_really_complicated_uuid",
        'resume_access': False,
    })

def sync_to_database(id):
    user = User.objects.get(pk=id)
    access = user.profile.resume_access

    ref = get_db_ref(f'users/{user.id}')
    ref.set({
        'resume_access': access,
    })
