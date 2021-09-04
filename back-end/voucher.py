
from login import *
import time
from datetime import date, datetime
from fuzzywuzzy import fuzz
from operator import itemgetter
import re
from collections import deque

class voucherHanlder():
    """
    This class is used for release voucher
    """
    # def __init__():
    #     pass

    def getTodayTimeStamp(self):

        real_time = datetime.today().strftime('%d-%m-%Y')
        real_array = time.strptime(real_time, "%d-%m-%Y")
        real_stamp = time.mktime(real_array)

        return real_stamp
    
    def timeStringToTimestamp_date(self, time_string):

        time_array = time.strptime(time_string, "%d-%m-%Y")
        time_stamp = time.mktime(time_array)

        return time_stamp

    def timeStringToTimestamp_time(self, time_string):

        time_array = time.strptime(time_string, "%H:%M")
        time_stamp = time.mktime(time_array)

        return time_stamp

    def timeStampToTimeString_date(self, time_stamp):
        """
        transfer date time stamp to date string
        """
        date_stamp = float(time_stamp)/1000
        date_array = datetime.fromtimestamp(date_stamp)
        date_string = date_array.strftime("%d-%m-%Y")

        return date_string

    def timeStampToTimeString_time(self, time_stamp):
        """
        transfer time stamp to time string
        """
        date_stamp = float(time_stamp)/1000
        date_array = datetime.fromtimestamp(date_stamp)
        date_string = date_array.strftime("%H:%M")

        return date_string

    def releaseVoucher(self, voucherInfo: dict):
        """
        store the voucher information in a dict and pass to this function
        """
        db = firestore.client()
        eatery_db = db.collection(u'eateries_login').document(voucherInfo['eatery_id'])
        eatery = eatery_db.get()
        eatery_info = eatery.to_dict()
        eatery_name = eatery_info['eateryName']

        print(voucherInfo['periodic'], type(voucherInfo['periodic']))

        voucher_date_string = self.timeStampToTimeString_date(voucherInfo['start_date'])
        start_time_string = self.timeStampToTimeString_time(voucherInfo['start_time'])
        end_time_string = self.timeStampToTimeString_time(voucherInfo['end_time'])

        print(voucher_date_string)

        voucher_db = eatery_db.collection(str(voucher_date_string))
        valid_time = start_time_string + "-" + end_time_string

        voucher_time = voucher_date_string + '_' + valid_time

        # eatery_info = eatery_db.get()

        date_collection = eatery_info['dateCollection']
        date_collection.append(voucher_time)
        eatery_db.update({
            u'dateCollection' : date_collection
        })

        if voucherInfo['periodic'] == 1:    # 1: it is a periodic voucher
            periodic_collection = eatery_info['periodicCollection']
            print(periodic_collection)
            periodic_collection.append(voucher_time)
            print(voucher_time)
            eatery_db.update({
                u'periodicCollection' : periodic_collection
            })

        for i in range(int(voucherInfo['amount'])):
            voucher_id = str(voucherInfo['eatery_id']) + '_' + voucher_time + '_' + str(i)
            db_ref = voucher_db.document(voucher_id)
            db_ref.set({
                u'voucher_id': voucher_id,
                u'eatery_id': voucherInfo['eatery_id'],
                u'eatery_name' : eatery_name,
                u'diner_id': None,
                u'start_date': voucher_date_string,
                u'start_time': start_time_string,
                u'end_time': end_time_string,
                u'discount': voucherInfo['discount'],
                u'periodic': voucherInfo['periodic'],
                u'status': None,
                u'review_rate': None,
                u'review_msg': None,
                u'userName': None,
                u'email': None
            })

    def releaseRepeatedVoucher(self, eatery_id):
        db = firestore.client()
        real_stamp = self.getTodayTimeStamp()

        eatery_db = db.collection(u'eateries_login').document(eatery_id)
        eatery = eatery_db.get()
        eatery_info = eatery.to_dict()
        periodic_collection = eatery_info['periodicCollection']

        stack = deque(periodic_collection)
        num = len(stack)

        for _ in range(num):
            date_time = stack.popleft()
            temp = date_time.split('_')
            date_string = temp[0]
            time_string = temp[1].split('-')
            date_stamp = self.timeStringToTimestamp_date(date_string)
            start_time = time_string[0]
            end_time = time_string[1]

            if date_stamp < real_stamp:
                voucher_info = {}
                voucher_db = eatery_db.collection(date_string)
                repeat_voucher = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).get()
                amount = len(repeat_voucher)
                repeat_voucher_info = repeat_voucher[0].to_dict()
                start_time_stamp = self.timeStringToTimestamp_time(start_time)
                end_time_stamp = self.timeStringToTimestamp_time(end_time)
                voucher_info['eatery_id'] = repeat_voucher_info['eatery_id']
                voucher_info['discount'] = repeat_voucher_info['discount']
                voucher_info['periodic'] = 1
                voucher_info['start_time'] = start_time_stamp * 1000
                voucher_info['end_time'] = end_time_stamp * 1000
                voucher_info['amount'] = amount
                voucher_info['start_date'] = (date_stamp + 86400 * 7) * 1000

                self.releaseVoucher(voucher_info)
                new_date = (date_stamp + 86400 * 7) * 1000
                new_date_string = self.timeStampToTimeString_date(new_date)
                new_date_time = new_date_string + '_' + temp[1]
                stack.append(new_date_time)
            else:
                stack.append(date_time)
        
        new_array = list(stack)
        eatery_db.update({
            u'periodicCollection' : new_array
        })

    @staticmethod
    def deleteRepeatedVoucher(voucher_id):
        db = firestore.client()

        voucher_info = voucher_id.split("_")
        delete_id = voucher_info[1] + '_' + voucher_info[2]
        eatery_id = voucher_info[0]
        
        eatery = db.collection(u'eateries_login').document(eatery_id)
        eatery_db = eatery.get()
        eatery_info = eatery_db.to_dict()

        periodic_collection = list(eatery_info['periodicCollection'])
        periodic_collection.remove(delete_id)

        voucher = eatery.collection(voucher_info[1])
        time_col = voucher_info[2].split('-')
        voucher_db = voucher.where(u'start_time', u'==', time_col[0]).where(u'end_time', u'==', time_col[1]).get()

        for i in range(len(voucher_db)):
            upgrade = voucher.document(voucher_db[i].id)
            upgrade.update({
                u'periodic' : 0
            })

        eatery.update({
                u'periodicCollection': periodic_collection
            })

    def eateryCheckVoucher(self, voucher_check):
        '''
        eatery check the voucher that provided by a diner
        check the date firstly and then check the eatery
        '''
        db = firestore.client()

        time_array = time.strptime(voucher_check['date'], "%d-%m-%Y")
        time_stamp = time.mktime(time_array)

        real_stamp = self.getTodayTimeStamp()

        if time_stamp == real_stamp:
            voucher_db = db.collection(u'eateries_login').document(voucher_check['eatery_id']).collection(voucher_check['date']).document(voucher_check['voucher_id'])
            voucher_db_info = voucher_db.get()
            voucher_diner = str(voucher_db_info.to_dict()['diner_id'])

            diner_db = db.collection(u'diner_login').document(voucher_diner).collection(u'voucher').document(voucher_check['voucher_id'])

            voucher_db.update({'status': 'checked'})
            diner_db.update({'status': 'checked'})
            
            return 0
        else:
            return 2
    
    # def voucherBasic(self, eatery_id, date, start_time, end_time, status):
    def voucherBasic(self, eatery_id, date, start_time, end_time):
        db = firestore.client()
        voucher_db = db.collection(u'eateries_login').document(eatery_id).collection(date)
        total_num = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).get()
        # status_num = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).where(u'status', u'==', status).get()

        booked_num = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).where(
            u'status', u'==', "booked").get()
        checked_num = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).where(
            u'status', u'==', "checked").get()

        doc = voucher_db.document(total_num[0].id).get()
        doc_info = doc.to_dict()
        periodic = doc_info['periodic']

        result = {}
        result['date'] = date
        result['startTime'] = start_time
        result['endTime'] = end_time
        result['total'] = len(total_num)
        # result[status] = len(status_num)
        result['booked'] = len(booked_num)
        result['checked'] = len(checked_num)
        result['periodic'] = periodic

        return result

    def voucherComment(self, eatery_id, date, start_time, end_time):
        db = firestore.client()
        voucher_db = db.collection(u'eateries_login').document(eatery_id).collection(date)
        voucher_comment = voucher_db.where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).where(u'status', u'==', 'checked').get()

        result = []

        for voucher_comment_info in voucher_comment:
            voucher = voucher_comment_info.to_dict()
            if voucher['review_rate']:
                item = {}
                item['date'] = date
                item['userName'] = voucher['userName']
                item['email'] = voucher['email']
                item['comment'] = voucher['review_msg']
                item['rate'] = voucher['review_rate']

                result.append(item)
        
        return result

    def extract(self, array, date_string):
        
        result = []
        for item_dict in array:
            if item_dict['date'] == date_string:
                result.append(item_dict)
        
        return result


    def eateryValidVoucher(self, eatery_id, search_date = None):
        '''
        eatery traverse the database, return how many voucher is valid from now on
        '''
        db = firestore.client()
        real_stamp = self.getTodayTimeStamp()

        eatery_db = db.collection(u'eateries_login').document(eatery_id)
        eatery_info = eatery_db.get()
        date_collection = eatery_info.to_dict()['dateCollection']
        valid = []
        history = []
        comment = []

        for item in date_collection:

            match_info = re.match(r"(.*)(\_)(.*)(\-)(.*)", item)
            date = match_info.group(1)
            date_stamp = self.timeStringToTimestamp_date(date)
            start_time = match_info.group(3)
            end_time = match_info.group(5)
            if date_stamp >= real_stamp:
                # valid
                # valid_info = self.voucherBasic(eatery_id, date, start_time, end_time, 'booked')
                valid_info = self.voucherBasic(eatery_id, date, start_time, end_time)
                valid.append(valid_info)
            else:
                # history
                # history_info = self.voucherBasic(eatery_id, date, start_time, end_time, 'checked')
                history_info = self.voucherBasic(eatery_id, date, start_time, end_time)
                history.append(history_info)
            # comment  
            comment_info = self.voucherComment(eatery_id, date, start_time, end_time)
            comment.append(comment_info)

        
        flat_comment = sum(comment, [])

        if search_date:
            search_date_string = self.timeStampToTimeString_date(search_date)
            # print(search_date_string)
            valid = self.extract(valid, search_date_string)
            history = self.extract(history, search_date_string)
            flat_comment = self.extract(flat_comment, search_date_string)

        # print(valid)

        return valid, history, flat_comment

class voucherQuery():
    '''
    search voucher
    '''
    # def __init__():
    #     pass

    def dinerCheckVoucher(self, voucher_book):
        """
        it is used to check the voucher records of a diner when he wants to book a new voucher,
        One customer can book only one type of voucher,
        if he already booked one voucher at a specific time, can't book more
        """
        db = firestore.client()
        diner_db = db.collection(u'diner_login').document(voucher_book['diner_id']).collection(u'voucher')
        start_date = voucher_book['date']
        start_time = voucher_book['start_time']
        end_time = voucher_book['end_time']

        voucher = diner_db.where(u'start_date', u'==', start_date).where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).get()

        if voucher:
            # already booked
            return True
        else:
            # haven't booked
            return False

    def dinerBookVoucher(self, voucher_book):
        """
        this function is used to book a new voucher for a diner at a specific time
        """
        db = firestore.client()

        voucher_db = db.collection(u'eateries_login').document(voucher_book['eatery_id']).collection(voucher_book['date'])
        start_time = voucher_book['start_time']
        end_time = voucher_book['end_time']
        vouchers = voucher_db.where(u'diner_id', u'==', None).where(u'start_time', u'==', start_time).where(u'end_time', u'==', end_time).get()

        diner_db = db.collection(u'diner_login').document(voucher_book['diner_id']).get()
        diner_info = diner_db.to_dict()
        diner_userName = diner_info['userName']
        email = diner_info['email']

        if not self.dinerCheckVoucher(voucher_book):
            voucher_db.document(vouchers[0].id).update({
                u'diner_id': voucher_book['diner_id'],
                u'status': 'booked',
                u'email': email,
                u'userName': diner_userName
            })

            doc = voucher_db.document(vouchers[0].id).get()
            doc_info = doc.to_dict()
            print(doc_info['voucher_id'], doc_info['eatery_name'])

            return doc_info['voucher_id'], doc_info['eatery_name']
        else:
            return 2, None
    
    def updateAvgReview(self, voucher_review):

        db = firestore.client()

        eatery_db = db.collection(u'eateries_login').document(voucher_review['eatery_id'])
        eatery_info = eatery_db.get()
        eatery_field = eatery_info.to_dict()
        num, score = int(eatery_field['peopleReviewed']), eatery_field['avgReview']

        if num == 0:
            num = 1
            score = float(voucher_review['rate'])
            # print(num, score)
        else:
            score = (float(score) * int(num) + float(voucher_review['rate'])) / (int(num) + 1)
            score = round(score, 2)    
            num = int(num) + 1

        eatery_db.update({
            'peopleReviewed': num,
            'avgReview': score
            })

        return 
    
    def dinerReviewVoucher(self, voucher_review):
        db = firestore.client()

        voucher_db = db.collection(u'eateries_login').document(voucher_review['eatery_id']).collection(voucher_review['date']).document(voucher_review['voucher_id'])
        diner_db = db.collection(u'diner_login').document(voucher_review['diner_id']).collection(u'voucher').document(voucher_review['voucher_id'])

        voucher_db_info = voucher_db.get()
        voucher_diner = str(voucher_db_info.to_dict()['diner_id'])
        if voucher_diner == voucher_review['diner_id']:
            self.updateAvgReview(voucher_review)
            diner_db.update({
                u'review_rate': float(voucher_review['rate']),
                u'review_msg': voucher_review['msg']
                })
            voucher_db.update({
                'review_rate': float(voucher_review['rate']),
                'review_msg': voucher_review['msg']
                })
            return 0
        else:
            return 3

    def dinerRecoredVoucher(self, voucher_id, eatery_name, voucher_book):
        db = firestore.client()
        diner_db = db.collection(u'diner_login').document(voucher_book['diner_id']).collection(u'voucher').document(voucher_id)
        timeHandler = voucherHanlder()
        date_stamp = timeHandler.timeStringToTimestamp_date(voucher_book['date'])

        return diner_db.set({
                u'voucher_id': voucher_id,
                u'diner_id': voucher_book['diner_id'],
                u'start_date': voucher_book['date'],
                u'start_time': voucher_book['start_time'],
                u'end_time': voucher_book['end_time'],
                u'date_stamp': date_stamp,
                u'status': 'booked',
                u'review_rate': None,
                u'review_msg': None,
                u'eatery_name': eatery_name
            })

    def dinerValidVoucher(self, diner_id, date):
        '''
        diner traverse the database, return how many voucher is valid from now on
        '''
        db = firestore.client()
        diner_db = db.collection(u'diner_login').document(diner_id).collection(u'voucher')
        # print("ok")
        timeHandler = voucherHanlder()
        today_stamp = timeHandler.getTodayTimeStamp()
        

        if not date:
            valid_vouchers = diner_db.where(u'date_stamp', u'>=', today_stamp).get()
        else:
        	date_string = timeHandler.timeStampToTimeString_date(date)
        	valid_vouchers = diner_db.where(u'status', u'==', 'booked').where(u'start_date', u'==', date_string).get()

        result = []
        for voucher_doc in valid_vouchers:
            temp = {}
            voucher = voucher_doc.to_dict()
            if voucher['status'] == 'booked':
            	temp['eateryName'] = voucher['eatery_name']	
            	temp['date'] = voucher['start_date']	
            	temp['startTime'] = voucher['start_time']
            	temp['endTime'] = voucher['end_time']
            	temp['voucher_id'] = voucher['voucher_id']
            if temp:
                result.append(temp)
        
        return result

    def dinerCheckedVoucher(self, diner_id, date):
        '''
        diner traverse the database, return how many voucher is valid from now on
        '''
        db = firestore.client()
        diner_db = db.collection(u'diner_login').document(diner_id).collection(u'voucher')
        # print("ok")
        timeHandler = voucherHanlder()
        today_stamp = timeHandler.getTodayTimeStamp()

        if not date:
            valid_vouchers = diner_db.where(u'date_stamp', u'<=', today_stamp).get()
        else:
        	date_string = timeHandler.timeStampToTimeString_date(date)
        	valid_vouchers = diner_db.where(u'start_date', u'==', date_string).get()

        result = []
        for voucher_doc in valid_vouchers:
            temp = {}
            voucher = voucher_doc.to_dict()
            if voucher['status'] == 'checked':
                temp['eateryName'] = voucher['eatery_name']
                temp['date'] = voucher['start_date']
                temp['startTime'] = voucher['start_time']
                temp['endTime'] = voucher['end_time']
                temp['voucher_id'] = voucher['voucher_id']
                temp['rate'] = voucher['review_rate']
                temp['comment'] = voucher['review_msg']
            
            if temp:
                result.append(temp)
        
        return result
    
    def dinerOverduedVoucher(self, diner_id, date):
        '''
        diner traverse the database, return how many voucher is valid from now on
        '''
        db = firestore.client()
        diner_db = db.collection(u'diner_login').document(diner_id).collection(u'voucher')
        # print("ok")
        timeHandler = voucherHanlder()
        today_stamp = timeHandler.getTodayTimeStamp()

        if not date:
            valid_vouchers = diner_db.where(u'date_stamp', u'<', today_stamp).get()
        else:
        	date_string = timeHandler.timeStampToTimeString_date(date)
        	valid_vouchers = diner_db.where(u'start_date', u'==', date_string).get()

        result = []
        for voucher_doc in valid_vouchers:
            temp = {}
            voucher = voucher_doc.to_dict()
            if voucher['status'] == 'booked':
                temp['eateryName'] = voucher['eatery_name']
                temp['date'] = voucher['start_date']
                temp['startTime'] = voucher['start_time']
                temp['endTime'] = voucher['end_time']
            
            if temp:
                result.append(temp)
        
        return result


    @staticmethod
    def db_document_fetch(collect: str):
        return firestore.client().collection(collect)
        pass

    @staticmethod
    def search_voucher(eateries_document, result_dict: {}, user_search):
        """
        this function is used to search the desired result by "name", "region", "cuisine", "date", and sort
        """
        judgmentDic = {'region': False, 'cuisine': False, 'eateryName': True}
        result_item = ['id', 'eateryName', 'avatar', 'intro', 'avgReview']
        eateries_list = eateries_document.get()

        for eateries_id in eateries_list:
            for user_select_item in user_search:
                result_dict[eateries_id.to_dict()['eateryName']] = eateries_id.to_dict()
                flag = 0
                # region, cuisine, eateryName
                if (user_select_item in judgmentDic.keys()) and len(user_search.get(user_select_item)) > 0:
                    if eateries_id.to_dict()[user_select_item] not in user_search.get(user_select_item):
                        eateries_item = str(eateries_id.to_dict()[user_select_item]).lower()
                        search_item = str(user_search.get(user_select_item)).lower()
                        if judgmentDic[user_select_item] and (fuzz.ratio(eateries_item, search_item) > 70 or (search_item in eateries_item)):
                           pass
                        else:
                            result_dict.pop(eateries_id.to_dict()['eateryName'])
                            break

                # date
                if user_select_item == 'voucher_date' and len(user_search['voucher_date']) > 0:
                    uid = eateries_document.document(eateries_id._data['id'])
                    subcollect = uid.collection(user_search.get(user_select_item))
                    if (subcollect.get()):
                        pass
                    else:
                        result_dict.pop(eateries_id._data['eateryName'])
                        break
                pass
            pass
        result_list = []
        result_full_list = [x for x in result_dict.values()]
        # assign default value (0) for avgRate if no review yet.
        for d in result_full_list:
            d.update((k, 0) for k, v in d.items() if v == None)
        # sort
        if user_search['sort'] == "top":
            result_full_list = sorted(result_full_list, key=lambda r: r['avgReview'], reverse=True)
        elif user_search['sort'] == "default":
            pass
        for dict_item in result_full_list:
            result_list.append({key: value for key, value in dict_item.items() if key in result_item })
            pass
        return result_list

    @staticmethod
    def recommend_voucher(eatery_id, eateries_document):
        cuisine = firestore.client().collection(u'eateries_login').document(eatery_id).get().to_dict()['cuisine']
        result_dict = {}
        user_search = {}
        user_search['cuisine'] = [cuisine]
        user_search['sort'] = "top"
        search_result = voucherQuery.search_voucher(eateries_document, result_dict, user_search)
        search_result = [i for i in search_result if not (i['id'] == eatery_id)] # remove itself from the list
        if (len(search_result) == 0): # there is nothing in the return list
            search = {}
            result_dict = {}
            search['sort'] = "top"
            search_result = voucherQuery.search_voucher(eateries_document, result_dict, search)
        if (len(search_result) > 3):
            for i in range(3, len(search_result)):
                search_result.pop(3)
        return search_result