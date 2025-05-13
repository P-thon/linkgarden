#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com 
import secrets
from django.utils.html import escape
from django.utils import timezone
from listings.models import MyCaptcha
from listings.system_log import MyLog
class MyCaptchaAction:
    @staticmethod
    def generate_random_captcha():
        animal_list = ["1", "2", "3", "4", "5"]
        captcha = ""
        subject = secrets.choice(animal_list)
        for x in range(9):
            captcha = captcha + secrets.choice(animal_list)
        check_answer_captcha = list(captcha)
        answer = ""
        for i, res in enumerate(check_answer_captcha):
            if res[0] == subject:
                answer = answer + str(i + 1)
        if subject not in captcha:
            MyCaptchaAction.generate_random_captcha()
        return [subject, captcha, answer]
    @staticmethod
    def generate_captcha_view(result : list):
        random_bird = ["aOHywdSN","dUGwiRvK","vMoOPNfn","zPoDuyOT","kTMpTegO","OGyzAYnf","yoicCAAH","ZXdlKnZc","hvbAODwV"]
        random_cat =  ["qGyUCMvk","VGsAnmcZ","REwkDsBg","MsPmOxxP","nAStmYVi","pcoIJUIx","FyolHeUS","sXXyRYox","lCLoQyaQ"]
        random_fish = ["MzCsWgdR","LpiFZiJe","EDVootUg","vMGmZmDr","TyRVLdip","ykXyEYfY","NXWvrzcL","ghWZvvXC","ATmlsAaX"]
        random_horse= ["LhRLzwfI","fdlHKiLG","rldoTLPB","skMquBUZ","jpBYuEEc","pTlGvFJq","BpvVtRHg","lbMbhKEM","yRTvJnnH"]
        random_lion = ["IlzgjBZR","VQVqvvdK","JnCXhqxU","euKnToSZ","TxFzlMoI","lTSbtkFH","MdOztjIG","SMfBudOt","sNKscYnK"]
        match result[0]:
            case "1":
                subject = "BIRD" 
            case "2":
                subject = "CAT" 
            case "3":
                subject = "FISH" 
            case "4":
                subject = "HORSE" 
            case "5":
                subject = "LION" 
            case default:
                subject = None
        img = []
        img_status = True
        if len(result[1]) != 9:
            img = None
        for x in list(result[1]):
            if x == "1":
                to_add = secrets.choice(random_bird)
                img.append(to_add)
                if to_add in random_bird:
                    random_bird.pop(random_bird.index(to_add))
            elif x == "2":
                to_add = secrets.choice(random_cat)
                img.append(to_add)
                if to_add in random_cat:
                    random_cat.pop(random_cat.index(to_add))
            elif x == "3":
                to_add = secrets.choice(random_fish)
                img.append(to_add)

                if to_add in random_fish:
                    random_fish.pop(random_fish.index(to_add))
            elif x == "4":
                to_add = secrets.choice(random_horse)
                img.append(to_add)
                if to_add in random_horse:
                    random_horse.pop(random_horse.index(to_add))
            elif x == "5":
                to_add = secrets.choice(random_lion)
                img.append(to_add)
                if to_add in random_lion:
                    random_lion.pop(random_lion.index(to_add))
            else:
                img_status = None
        if subject is None or img_status is None:
            return None
        return [subject, img]
    @staticmethod
    def compile_captcha_code(request):
        code = ""
        try:
            if request['cb1'] == "on":
                code = code + "1"
        except:
            pass
        try:
            if request['cb2'] == "on":
                code = code + "2"
        except:
            pass
        try:
            if request['cb3'] == "on":
                code = code + "3"
        except:
            pass
        try:
            if request['cb4'] == "on":
                code = code + "4"
        except:
            pass
        try:
            if request['cb5'] == "on":
                code = code + "5"
        except:
            pass
        try:
            if request['cb6'] == "on":
                code = code + "6"
        except:
            pass
        try:
            if request['cb7'] == "on":
                code = code + "7"
        except:
            pass
        try:
            if request['cb8'] == "on":
                code = code + "8"
        except:
            pass
        try:
            if request['cb9'] == "on":
                code = code + "9"
        except:
            pass
        if len(code) == 0 or code is None:
            return 0
        return code
    @staticmethod
    def add_captcha_in_db(request):
        try:
            captcha_data = MyCaptchaAction.generate_random_captcha()
            MyCaptcha(key=request.session.session_key,subject=escape(captcha_data[0]),answer=escape(captcha_data[1]),response=escape(captcha_data[2]),date=timezone.now()).save()
            return captcha_data
        except:
            return None
    @staticmethod
    def get_captcha(request) -> list:
        if MyCaptcha.objects.filter(key = request.session.session_key).count() != 0:
            try:
                data = MyCaptcha.objects.filter(key = request.session.session_key).values("subject", "answer").order_by('-date')[:1].get()
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.30 > Can't get MyCaptcha.")
                request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
                return None
            captcha_view = MyCaptchaAction.generate_captcha_view([data['subject'], data['answer']])
            if captcha_view is None or len(captcha_view) != 2 or len(captcha_view[1]) != 9:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.31 > Can't generate captcha view.")
                request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
                return None
            return captcha_view
        result_captcha = MyCaptchaAction.add_captcha_in_db(request)
        if result_captcha is None:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.32 > Can't add captcha view in verification.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            return None
        captcha_view = MyCaptchaAction.generate_captcha_view(result_captcha)
        if captcha_view is None or len(captcha_view) != 2 or len(captcha_view[1]) != 9:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.33 > Can't generate captcha view in verification.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            return None
        return captcha_view
    @staticmethod
    def reset_captcha(request) -> list:
        result_captcha = MyCaptchaAction.add_captcha_in_db(request)
        if result_captcha is None:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.34 > Can't add captcha view in verification.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            return None
        captcha_view = MyCaptchaAction.generate_captcha_view(result_captcha)
        if captcha_view is None or len(captcha_view) != 2 or len(captcha_view[1]) != 9:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.35 > Can't generate captcha view in verification.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            return None
        return captcha_view
    @staticmethod
    def verif_captcha(request) -> bool:
        try:
            input_captcha = MyCaptchaAction.compile_captcha_code(request.POST)
            result_captcha = MyCaptcha.objects.filter(key = request.session.session_key).values("response").order_by('-date')[:1].get()
            if result_captcha['response'] == "" or result_captcha is None:
                result_captcha['response'] = 0
            if input_captcha != result_captcha['response']:
                request.session['status'] = ["Invalid captcha.", "red", True]
                return False
            return True
        except:
            return None