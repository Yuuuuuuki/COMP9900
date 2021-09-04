from types import resolve_bases
from typing import Collection, ItemsView
import tornado.web
import tornado.ioloop
import json
from login import *
from admin import *
import os
from voucher import *
import re
from datetime import datetime

import mysession
class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = mysession.Session(self)

# redirect
class dinerRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class eateryRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("eatery.html")

class adminRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("admin.html")

# user login handler
class UserloginHandler(tornado.web.RequestHandler):

    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')
        password = json_args.get('password')
        role = json_args.get('role')

        login = loginHandler()
        check_exist = RegisterDBHandler()

        try:
            user = login.loginMethod(email, password)
            user_id = user['localId']
            if role == 'diner':
                if check_exist.db_check('diner_login', user_id):
                    ret = {'result': 0} # success
                    ret['ID'] = user_id
                else:
                    ret = {'result': 1} #fail
            elif role == 'eatery':
                repeatVoucherHanlder = voucherHanlder()
                if check_exist.db_check('eateries_login', user_id):
                    ret = {'result': 0} # success
                    repeatVoucherHanlder.releaseRepeatedVoucher(user_id)
                    ret['ID'] = user_id
                else:
                    ret = {'result': 1} #fail
            elif role == 'admin':
                if check_exist.db_check('admin_login', user_id):
                    ret = {'result': 0} # success
                    ret['ID'] = user_id
                else:
                    ret = {'result': 1} #fail
        except:
            ret = {'result': 1} #fail
        
        self.write(json.dumps(ret))

class LogoutHandler(tornado.web.RequestHandler):
  def post(self):
    mysession.Session.delete()
    self.render("index.html")

# upload file handler
class UploadfileHandler(tornado.web.RequestHandler):

    # testing upload
    def get(self):
        self.write("""<form action='file' enctype="multipart/form-data" method='post'>
                    <p> <input type='file' name='file' /></p>
                    <p><input type='submit' value='submit' /></p>
                    </form>""")
        # print("ok")

    def post(self):
        ret = {'result': 0} # success
        file_metas = self.request.files.get('file', None)

        if not file_metas:
            ret['result'] = 1
            return ret
        
        upload = fileHandler(file_metas)
        if upload.upload():
            file_url = upload.upload()
            ret['url'] = file_url
        else:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# user reset password handler
class ResetPassword(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')
        reset = loginHandler()
        try:
            reset.resetPassword(email)
            ret = {'result': 0}  # success
        except:
            ret = {'result': 1}  # fail

        self.write(json.dumps(ret))

# diner register
class DinerRegHandler(tornado.web.RequestHandler):

    def post(self):
        # print(self.request.headers.get("Content-Type"))
        ret = {'result': 0} # success
        
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')
        password = json_args.get('password')
        userName = json_args.get('userName')
        firstName = json_args.get('firstName')
        familyName = json_args.get('familyName')
        preference = json_args.get('preference')

        diner_register = loginHandler()
        try:
            new_user = diner_register.register(email, password)
            dinerID = new_user['localId']
            ret = {'result': 0} # success
        except:
            ret = {'result': 2} # account already exist, return
            self.write(json.dumps(ret))
            return

        # if it is a new account, add to database
        diner_Reg_DB = RegisterDBHandler()
        try:
            diner_Reg_DB.diner_add(dinerID, email, password, userName, firstName, familyName, preference)
            ret = {'result': 0} # success
            ret['ID'] = dinerID
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# eatery register handler
class EateryRegHandler(tornado.web.RequestHandler):
    def post(self):
        # print(self.request.headers.get("Content-Type"))
        ret = {'result': 0} # success
        
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')
        password = json_args.get('password')
        eateryName = json_args.get('eateryName')
        region = json_args.get('region')
        street = json_args.get('street')
        cuisine = json_args.get('cuisine')
        menu = json_args.get('menu')

        eatery_register = loginHandler()
        try:
            new_user = eatery_register.register(email, password)
            eateryID = new_user['localId']
            ret = {'result': 0} # success
        except:
            ret = {'result': 2} # account already exist, return
            self.write(json.dumps(ret))
            return

        # if it is a new account, add to database
        eatery_Reg_DB = RegisterDBHandler()
        try:
            eatery_Reg_DB.eatery_add(email, password, eateryName, region, street, cuisine, eateryID, menu)
            ret = {'result': 0} # success
            ret['ID'] = eateryID
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# diner update his/her profile
class DinerUpdateHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {'result': 0} # success
        
        json_data = self.request.body
        json_args = json.loads(json_data)

        update = {}
        update['avatar'] = json_args.get('avatar')
        update['userName'] = json_args.get('userName')
        update['firstName'] = json_args.get('firstName')
        update['familyName'] = json_args.get('familyName')
        update['preference'] = json_args.get('preference')
        update['id'] = json_args.get('id')
        

        # update the info of diner by using update
        try:
            RegisterDBHandler.update('diner_login', update)
            ret = {'result': 0} # success
            ret['ID'] = update['id']
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# eatery update his/her profile handler
class EateryUpdateHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {'result': 0} # success
        
        json_data = self.request.body
        json_args = json.loads(json_data)

        update = {}
        update['avatar'] = json_args.get('avatar')
        update['eateryName'] = json_args.get('eateryName')
        update['region'] = json_args.get('region')
        update['street'] = json_args.get('street')
        update['cuisine'] = json_args.get('cuisine')
        update['menu'] = json_args.get('menu')
        update['id'] = json_args.get('id')
        update['intro'] = json_args.get('intro')

        # update the info of diner by using update
        try:
            RegisterDBHandler.update('eateries_login', update)
            ret = {'result': 0} # success
            ret['ID'] = update['id']
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# list out all the cuisines
class CuisineListHandler(tornado.web.RequestHandler):
    def get(self):
        cuisine = RegisterDBHandler.DB_traversal("type", "cuisine")
        self.write(json.dumps(cuisine))

# list out the regions
class RegionListHandler(tornado.web.RequestHandler):
    def get(self):
        region = RegisterDBHandler.DB_traversal("type", "region")
        self.write(json.dumps(region))

# get user information based on role (diner or eatery)
class UserInfoHandler(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        user = json_args.get('role')
        id = json_args.get('id')

        if user == "diner":
            col = "diner_login"
        else:
            col = "eateries_login"

        user_info = RegisterDBHandler.DB_traversal(col, id)
        self.write(json.dumps(user_info))

# search function by eatery name
class SearchEatery(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_name = json_args.get('eatery')

        search_db = RegisterDBHandler()
        eatery_info = search_db.DB_traversal_item('eateries_login', item = eatery_name)
        if eatery_info:
            self.write(json.dumps(eatery_info))
            return 
        else:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))
            return 

# search eatery by details (location, cuisine type and valid voucher date)
class DetailSearchEatery(tornado.web.RequestHandler):
    # return : eatery name, eatery avatar, voucher start time & voucher end time
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        result_dict = {}
        user_search = {}
        region = []
        user_search['eateryName'] = json_args.get('eatery')
        user_search['cuisine'] = json_args.get('cuisine')
        # user_search['region'] = json_args.get('region')
        if json_args.get('region') != None:
            region.append(json_args.get('region'))
        user_search['region'] = region
        timestring = json_args.get('date')

        if isinstance(timestring, int):
            timestring = float(timestring) / 1000
            date = datetime.fromtimestamp(timestring).strftime("%d-%m-%Y")
            user_search['voucher_date'] = date
        else:
            user_search['voucher_date'] = ""

        # if isinstance(region, str):
        #     user_search['region'] = region
        # else:
        #     user_search['region'] = ""


        user_search['sort'] = json_args.get('sort')
        eateries_document = voucherQuery.db_document_fetch('eateries_login')
        search_result = voucherQuery.search_voucher(eateries_document, result_dict, user_search)
        # sort
        self.write(json.dumps(search_result))

# eatery release vouchers based on date, time, discount, amount and periodic
class ReleaseVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        voucher_info = {}
        voucher_info['eatery_id'] = json_args.get('id')
        voucher_info['start_date'] = json_args.get('date')
        voucher_info['start_time'] = json_args.get('startTime')
        voucher_info['end_time'] = json_args.get('endTime')
        voucher_info['discount'] = json_args.get('discount')
        voucher_info['amount'] = json_args.get('amount')
        voucher_info['periodic'] = json_args.get('everyWeekFlag')

        voucher_db = voucherHanlder()

        try:
            voucher_db.releaseVoucher(voucher_info)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# diner books a voucher base on eatery, date and time
class DinerBookVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        voucher_book = {}
        voucher_book['eatery_id'] = json_args.get('eatery_id')
        voucher_book['diner_id'] = json_args.get('diner_id')

        # test string input
        voucher_book['date'] = json_args.get('date')
        voucher_book['start_time'] = json_args.get('startTime')
        voucher_book['end_time'] = json_args.get('endTime')

        #test time stamp input
        # time_transfer = voucherHanlder()
        # voucher_book['date'] = time_transfer.timeStampToTimeString_date(json_args.get('date'))
        # voucher_book['start_time'] = time_transfer.timeStampToTimeString_date(json_args.get('startTime'))
        # voucher_book['end_time'] = time_transfer.timeStampToTimeString_date(json_args.get('endTime'))

        # voucher_book['firstName'] = json_args.get('firstName')
        # voucher_book['familyName'] = json_args.get('familyName')
        # voucher_book['email'] = json_args.get('email')
        # voucher_book['phoneNumber'] = json_args.get('phoneNumber')
        # voucher_book['peopleNumber'] = json_args.get('peopleNumber')

        query_voucher = voucherQuery()

        try:
            result_id, result_name = query_voucher.dinerBookVoucher(voucher_book)
            if result_id == 2:
                ret = {'result': 2} # already booked
                self.write(json.dumps(ret))
                return
            else:
                # result_id, result_name = query_voucher.dinerBookVoucher(voucher_book)
                query_voucher.dinerRecoredVoucher(result_id, result_name, voucher_book)
                ret = {'result': 0} # success
                ret['booked_id'] = str(result_id)
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# eatery check out a voucher for a diner
class EateryCheckVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        voucher_check = {}
        voucher_check['voucher_id'] = json_args.get('voucher_id')
        voucher_check['eatery_id'] = json_args.get('eatery_id')

        match_info = re.match(r"(\w+)(\_)(.*)(\_)(.*)(\_)(\w+)", voucher_check['voucher_id'])

        if voucher_check['eatery_id'] != match_info.group(1):
            ret = {'result': 4} # the given eatery id doesn't match the eatery id on the voucher, this voucher can not be used in this restuarant
            self.write(json.dumps(ret))
            return 

        voucher_check['eatery_id'] = match_info.group(1)
        voucher_check['date'] = match_info.group(3)

        check_voucher = voucherHanlder()

        try:
            if check_voucher.eateryCheckVoucher(voucher_check) == 0:
                ret = {'result': 0} # success
            elif check_voucher.eateryCheckVoucher(voucher_check) == 2:
                ret = {'result': 2} # not valid today
            else:
                ret = {'result': 3} # differnt diner
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# diner review a used voucher
class DinerReviewVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        voucher_review = {}
        voucher_review['voucher_id'] = json_args.get('voucher_id')
        voucher_review['diner_id'] = json_args.get('diner_id')
        voucher_review['rate'] = json_args.get('rate')
        voucher_review['msg'] = json_args.get('comment')

        match_info = re.match(r"(\w+)(\_)(.*)(\_)(.*)(\_)(\w+)", voucher_review['voucher_id'])
        voucher_review['eatery_id'] = match_info.group(1)
        voucher_review['date'] = match_info.group(3)

        check_voucher = voucherQuery()

        try:
            if check_voucher.dinerReviewVoucher(voucher_review) == 0:
                ret = {'result': 0} # success
            else:
                ret = {'result': 3} # differnt diner
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# list out all the valid voucher for a eatery
class EateryValidVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_id = json_args.get('eatery_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherHanlder()
        try:
            valid, history, comment = voucher_db.eateryValidVoucher(eatery_id, date)
            self.write(json.dumps(valid))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out the voucher history for eatery
class EateryHistoryVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_id = json_args.get('eatery_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherHanlder()
        try:
            valid, history, comment = voucher_db.eateryValidVoucher(eatery_id, date)
            self.write(json.dumps(history))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out all the comments from diners
class EateryCommentVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_id = json_args.get('eatery_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherHanlder()
        try:
            valid, history, comment = voucher_db.eateryValidVoucher(eatery_id, date)
            self.write(json.dumps(comment))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out all the valid vouchers for a diner who already booked
class DinerValidVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        diner_id = json_args.get('diner_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherQuery()
        try:
            valid = voucher_db.dinerValidVoucher(diner_id, date)
            self.write(json.dumps(valid))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out all the used vouchers for a diner
class DinerCheckedVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        diner_id = json_args.get('diner_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherQuery()
        try:
            valid = voucher_db.dinerCheckedVoucher(diner_id, date)
            self.write(json.dumps(valid))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out all the expired vouchers for a diner 
class DinerOverduedVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        diner_id = json_args.get('diner_id')
        date = json_args.get('date') # time stamp

        voucher_db = voucherQuery()
        try:
            valid = voucher_db.dinerOverduedVoucher(diner_id, date)
            self.write(json.dumps(valid))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# admin can delete the region in database
class DeleteRegion(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        region_id = json_args.get('region_id')

        try:
            regioncuisineHandler.deleteitem("region", region_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# admin can delete the cuisine from cuisine list
class DeleteCuisine(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        cuisine_id = json_args.get('cuisine_id')

        try:
            regioncuisineHandler.deleteitem("cuisine", cuisine_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# admin can add regions in the database
class AddRegion(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        region_name = json_args.get('name')

        try:
            regioncuisineHandler.additem("region", region_name)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# admin can add cuisine in the cuisine list
class AddCuisine(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        cuisine_name = json_args.get('name')

        try:
            regioncuisineHandler.additem("cuisine", cuisine_name)
            ret = {'result': 0} # success
        except Exception as e:
            print(str(e))
            print(e.with_traceback())
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# admin can update the region info in database
class UpdateRegion(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        region_name = json_args.get('name')
        region_id = json_args.get('id')

        try:
            regioncuisineHandler.updateitem("region", region_name, region_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# admin can update the cuisine info
class UpdateCuisine(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        cuisine_name = json_args.get('name')
        cuisine_id = json_args.get('id')

        try:
            regioncuisineHandler.updateitem("cuisine", cuisine_name, cuisine_id)
            ret = {'result': 0} # success
        except Exception as e:
            print(str(e))
            print(e.with_traceback())
            ret = {'result': 1} #fail

        self.write(json.dumps(ret))

# list out all the diners in admin page
class AdminDiner(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')

        db = RegisterDBHandler()
        try:
            result = db.DB_traversal_email(email, 'diner_login')
            self.write(json.dumps(result))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# list out all the eateries in admin page
class AdminEatery(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        email = json_args.get('email')

        db = RegisterDBHandler()
        try:
            result = db.DB_traversal_email(email, 'eateries_login')
            self.write(json.dumps(result))
        except:
            ret = {'result': 1} #fail
            self.write(json.dumps(ret))

# admin have access to delete diner and eatery
class AdminDeleteDiner(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        diner_id = json_args.get('diner_id')

        db = RegisterDBHandler()
        try:
            db.DB_delete('diner', diner_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail
        
        self.write(json.dumps(ret))

class AdminDeleteEatery(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_id = json_args.get('eatery_id')

        db = RegisterDBHandler()
        try:
            db.DB_delete('eatery', eatery_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail
        
        self.write(json.dumps(ret))

# recommendation system
class Recommendation(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        eatery_id = json_args.get('eatery_id')
        eateries_document = voucherQuery.db_document_fetch('eateries_login')
        search_result = voucherQuery.recommend_voucher(eatery_id, eateries_document)

        self.write(json.dumps(search_result))

# eatery can cancel the periodic voucher
class EateryDeletePeriodicVoucher(tornado.web.RequestHandler):
    def post(self):
        json_data = self.request.body
        json_args = json.loads(json_data)

        voucher_id = json_args.get('voucher_id')
        print(voucher_id)

        try:
            voucherHanlder.deleteRepeatedVoucher(voucher_id)
            ret = {'result': 0} # success
        except:
            ret = {'result': 1} #fail
        
        self.write(json.dumps(ret))


if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r"/api/login", UserloginHandler),
            (r"/api/diner_register", DinerRegHandler),
            (r"/api/eatery_register", EateryRegHandler),
            (r"/api/reset_password", ResetPassword),
            (r"/api/diner_update", DinerUpdateHandler),
            (r"/api/eatery_update", EateryUpdateHandler),
            (r"/api/file", UploadfileHandler),
            (r"/api/get_cuisine_list", CuisineListHandler),
            (r"/api/get_region_list", RegionListHandler),
            (r"/api/get_user_info", UserInfoHandler),
            (r"/api/release_voucher", ReleaseVoucher),
            (r"/api/eatery_delete_periodic_voucher", EateryDeletePeriodicVoucher),
            (r"/api/diner_book_voucher", DinerBookVoucher),
            (r"/api/eatery_check_voucher", EateryCheckVoucher),
            (r"/api/diner_review_voucher", DinerReviewVoucher),
            (r"/api/eatery_valid_voucher", EateryValidVoucher),
            (r"/api/eatery_history_voucher", EateryHistoryVoucher),
            (r"/api/eatery_comment_voucher", EateryCommentVoucher),
            (r"/api/diner_valid_voucher", DinerValidVoucher),
            (r"/api/diner_checked_voucher", DinerCheckedVoucher),
            (r"/api/diner_overdued_voucher", DinerOverduedVoucher),
            (r"/api/search_eatery", SearchEatery),
            (r"/api/detail_search_eatery", DetailSearchEatery),
            (r"/api/delete_region", DeleteRegion),
            (r"/api/delete_cuisine", DeleteCuisine),
            (r"/api/add_region", AddRegion),
            (r"/api/add_cuisine", AddCuisine),
            (r"/api/update_region", UpdateRegion),
            (r"/api/update_cuisine", UpdateCuisine),
            (r"/api/admin_diner", AdminDiner),
            (r"/api/admin_eatery", AdminEatery),
            (r"/api/admin_delete_diner", AdminDeleteDiner),
            (r"/api/admin_delete_eatery", AdminDeleteEatery),
            (r"/api/recommendation", Recommendation),
            (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "dist/js"))),
            (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "dist/css"))),
            (r"/img/(.*)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "dist/img"))),
            (r"/eatery/*", eateryRequestHandler),
            (r"/admin/*", adminRequestHandler),
            (r"/*", dinerRequestHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "dist")
    )

    configHandler().fireadminInit()

    app.listen(8881)
    print("I am listening")
    tornado.ioloop.IOLoop.current().start()
