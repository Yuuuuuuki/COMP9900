import pyrebase
import urllib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import json

class configHandler():
    """
    This class is to config. firebase related function
    """
    def __init__(self):
        pass

    def readData(self, type):
        with open('config.json') as config_file:
            self.data = json.load(config_file)
            self.configData = self.data.get(type)
            return self.configData

    def pyrebaseInit(self):
        """
        inite pyerbase(A simple python wrapper for firebase) as it is required by firebase auth and storage
        """
        config = self.readData("pyrebaseconfig")
        self.firebase = pyrebase.initialize_app(config[0])
        return self.firebase

    def fireadminInit(self):
        """
        inite fireadmin as it is required by firestore
        """
        config = self.readData("fireadminconfig")
        cred = config[1]
        cred = cred.get("apikey")
        cred = credentials.Certificate(cred)
        self.fireadmin = firebase_admin.initialize_app(cred, config[0])
        return self.fireadmin


class loginHandler():
    def __init__(self):
        self.firebase = configHandler()
        self.firebase = self.firebase.pyrebaseInit() 
        # Get a reference to the auth service
        self.auth = self.firebase.auth()

    def loginMethod(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    def resetPassword(self, email):
        return self.auth.send_password_reset_email(email)

    def register(self, email, password):
        return self.auth.create_user_with_email_and_password(email, password)


class RegisterHandler():
    def __init__(self, email, password):
        self.firebase = configHandler()
        self.firebase = self.firebase.pyrebaseInit()
        self.auth = self.firebase.auth()
        self.email = email
        self.password = password

class fileHandler():
    def __init__(self, file_metas):
        self.firebase = configHandler()
        self.firebase = self.firebase.pyrebaseInit()
        self.storage = self.firebase.storage()
        self.file_metas = file_metas

    def upload(self):
        """
        upload file to firestore
        """
        filename = self.file_metas[0]["filename"]
        upload_file = self.file_metas[0]["body"]
        if filename[-3:] != "pdf":
            cloudfilename = "/test/img/" + self.file_metas[0]["filename"]
        else:
            cloudfilename = "/test/menu/"+ self.file_metas[0]["filename"]

        if self.storage.child(cloudfilename).put(upload_file):
            return self.storage.child(cloudfilename).get_url(None)
        else:
            return False
        
class RegisterDBHandler():
    # use to check if a document exists in a collection
    def db_check(self, collection, document, collection2 = None):
        db = firestore.client()

        if not collection2:
            doc_ref = db.collection(collection).document(document)
            doc = doc_ref.get()
            if doc.exists:
                return True
            else:
                return False

    def diner_add(self, dinerID, email, password, userName, firstName, familyName, preference):
        doc_ref = firestore.client().collection(u'diner_login').document(dinerID)
        return doc_ref.set({
            u'id': dinerID,
            u'email': email,
            u'password': password,
            u'userName': userName,
            u'firstName': firstName,
            u'familyName': familyName,
            u'preference': preference,
            u'avatar': None
        })

    def eatery_add(self, email, password, eateryName, region, street, cuisine, eateryID, menu):
        doc_ref = firestore.client().collection(u'eateries_login').document(eateryID)
        return doc_ref.set({
            u'id': eateryID,
            u'email': email,
            u'password': password,
            u'eateryName': eateryName,
            u'region': region,
            u'street': street,
            u'cuisine': cuisine,
            u'avatar': None,
            u'menu': menu,
            u'intro': None,
            u'dateCollection': [],
            u'periodicCollection': [],
            u'avgReview': None, # int, average rate score
            u'peopleReviewed': 0 # int, how many people have reviews so far
        })

    @staticmethod
    def update(client, update):

        updateID = update['id']

        doc_ref = firestore.client().collection(client).document(updateID)
        for item in update:
            if update[item]:
                doc_ref.update({item: update[item]})

    @staticmethod
    def DB_traversal(collect, document):
        # DB traversal for cuisine and region
        users_ref = firestore.client().collection(collect).document(document)
        doc = users_ref.get()
        real_doc = doc.to_dict()

        if document == "cuisine":
            rest = []
            for item in real_doc:
                temp = {}
                temp['name'] = real_doc[item]
                temp['id'] = item
                rest.append(temp)
            return rest

        elif document == "region":
            rest = []
            for item in real_doc:
                temp = {}
                temp['name'] = real_doc[item]
                temp['id'] = item
                rest.append(temp)
            return rest
        else:
            return real_doc

    def DB_traversal_item(self, collect, item = None):
        db = firestore.client()
        users_ref = db.collection(collect)
        docs = users_ref.stream()

        if not item:
            result = []
            for doc in docs:
                result.append(doc.to_dict())
            return result

        for doc in docs:
            if doc.to_dict()['eateryName'] == item:
                return doc.to_dict()

        return None
    
    def DB_traversal_email(self, email, collect):
        result = self.DB_traversal_item(collect)

        if email:
            real_result = []
            for doc in result:
                if doc['email'] == email:
                    real_result.append(doc)
            return real_result

        return result

    def DB_delete(self, role, delete_id):
        db = firestore.client()
        collect = 'diner_login' if role == 'diner' else 'eateries_login'
        db.collection(collect).document(delete_id).delete()


    def detail_DB_traversal(self, search):

        pass

