from voucher import *

class regioncuisineHandler:
    """
    This function is used by admin in order to update/delete/add region/cuisine info in the database
    """
    @staticmethod
    def updateitem(type, item, id):
        ref = firestore.client().collection('type').document(type)
        ref.update({id: item})

    @staticmethod
    def deleteitem(type, id):
        ref = firestore.client().collection('type').document(type)
        ref.update({id: firestore.DELETE_FIELD})

    @staticmethod
    def additem(type, item):
        ref = firestore.client().collection('type').document(type)
        ref_list = ref.get().to_dict()
        i = 1
        while True:
            if str(i) in ref_list:
                i = i + 1
            else:
                break
        data = {
           str(i): item
        }
        ref.set(data, merge=True)

