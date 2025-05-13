#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com 
from django.contrib.auth import authenticate, login, logout
from django.utils.html import escape
from django.utils import timezone
from listings.models import MyCaptcha, MyLinkBetweenUserAndSession, MyVerifCode
from listings.system_captcha import MyCaptchaAction
from listings.system_security import MySecurity
from listings.system_log import MyLog
from listings.system_external import MyExternalRequest
from listings.system_default import MyTime, MyRandom, MyCrypto
class MyLoginAction():
    @staticmethod
    def login_process(request):
        try:
            if MyTime.check_last_time_from_log(request, "ADMIN_LOGIN_SUBMIT", 10):
                MyLog.write_log(request.session.session_key, "ADMIN_LOGIN_SUBMIT")
                if MySecurity.verif_spam_action(request, 'ADMIN_LOGIN_SUBMIT', 5, 60):
                    request.session['SHADOW'] = True
                    MyLog.write_log(request.session.session_key, 'SHADOW_BAN_FROM_ADMINLOGIN')
                    request.session['status'] = ["You have been banned from admin-login. Try again later.", "red"]
                    MySecurity.update_score(request, "-", 50, "/")
                    return False
                request.session['status'] = ["Please wait before trying again.", "red", True]
                return True
            MyLog.write_log(request.session.session_key, "ADMIN_LOGIN_SUBMIT")
            if MySecurity.verif_spam_action(request, 'ADMIN_LOGIN_SUBMIT', 5, 60):
                request.session['SHADOW'] = True
                MyLog.write_log(request.session.session_key, 'SHADOW_BAN_FROM_ADMINLOGIN')
                return False
            captcha_status = MyCaptchaAction.verif_captcha(request)
            if captcha_status is None:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.10 > Can't verif captcha.")
                request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
                return True
            if captcha_status == False:
                return True
            for x in ["username", "password", "csrfmiddlewaretoken"]:
                try:
                    if request.POST[x] == "" or request.POST[x] == None or request.POST[x] == " ":
                        MySecurity.update_score(request, "-", 50, "/")
                        return False
                except:
                    MySecurity.update_score(request, "-", 50, "/")
                    return False
            username = escape(request.POST['username'])
            password = escape(request.POST['password'])
            user = authenticate(username = username, password = password)
            if user is None:
                MyLog.write_log(request.session.session_key, 'LOGIN_INVALID')
                request.session['status'] = ["Invalid username or password.", "red", True]
                return True
            MyCaptcha.objects.filter(key=request.session.session_key).all().delete()
            old_key = request.session.session_key
            login(request, user)
            MyLinkBetweenUserAndSession(
                userid = str(request.user.id),
                status = str("LOGIN"),
                old_key = str(old_key),
                new_key = str(request.session.session_key),
            ).save()
            jeton = MyRandom.get_random_number_str(9)
            enc_jeton = MyCrypto().sym_encrypt(jeton, "7RB3snJQy3p993AhN3F4a828PXuzpKgg")
            if MyExternalRequest.telegram_send(jeton) != True:
                request.session['status'] = ["Can't send telegram message. Please contact us.", "red"]
                return True
            MyVerifCode(
                key = request.session.session_key, 
                code = enc_jeton,
                date = timezone.now()
            ).save()
            request.session['2FA'] = "WAIT_FOR_2FA_CODE"
            MyLog.write_log(request.session.session_key, "LOGIN_OK")
            MyLog.notif(f"Someone requested a 2FA token. IP: {MySecurity.get_ip(request)} | User-Agent: {request.headers['User-Agent']}")
            request.session['status'] = ["Message perfectly send.", "green"]
            return True
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.11 > Error in login proccess.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red"]
            return None
    @staticmethod
    def twofactorauth_process(request):
        try:
            status_code = MySecurity.verif_2FA_code(request.POST, {'input' : ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "csrfmiddlewaretoken"]})
            if MyTime.check_last_time_from_log(request, "ADMIN_2FA_SUBMIT", 10) :
                request.session['status'] = ["Please wait before trying again.", "red"]
                return None
            MyLog.write_log(request.session.session_key, "ADMIN_2FA_SUBMIT")
            if status_code == False or len(str(status_code)) != 9:
                request.session['status'] = ["Invalid 2FA code.", "red"]
                return None
            result = MyVerifCode.objects.filter(key= request.session.session_key).get()
            enc_code = str(result.code)
            date = result.date
            if MyTime.time_checker(date, 300) != True:
                request.session['status'] = [f"Your code have expired.", "red"]
                return None
            if MyCrypto().sym_decrypt(enc_code, "7RB3snJQy3p993AhN3F4a828PXuzpKgg") != status_code:
                request.session['status'] = ["Invalid 2FA Code.", "red"]
                return None
            MyLog.write_log(request.session.session_key, "ADMIN_2FA_OK")
            request.session['2FA'] = True
            request.session['ADMIN'] = True
            MyVerifCode.objects.filter(key=request.session.session_key).all().delete()
            MyLog.notif(f"An administrator has just logged in. | IP: {MySecurity.get_ip(request)} | User-Agent: {request.headers['User-Agent']}")
            return True
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.12 > Error in 2FA process.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red"]
            return None
    @staticmethod  
    def twofactorauth_goback(request):
        try:
            if request.user.is_authenticated:
                MyVerifCode.objects.filter(key=request.session.session_key).all().delete()
                MyCaptcha.objects.filter(key=request.session.session_key).all().delete()
                MyLog.write_log(request.session.session_key, 'LOGOUT')
                user_id = request.user.id
                old_key = request.session.session_key
                old_score = request.session.get("SCORE", 0)
                logout(request)
                request.session.create()
                request.session['SCORE'] = old_score
                request.session['SHADOW'] = False
                request.session['FULLBAN'] = False
                request.session['ADMIN'] = False
                request.session['2FA'] = False
                request.session['CURRENT_HEADER'] = request.headers['User-Agent']
                request.session['CURRENT_IP'] = MySecurity.get_ip(request)
                MyLinkBetweenUserAndSession(
                    userid = str(user_id),
                    status = str("LOGOUT"),
                    old_key = str(old_key),
                    new_key = str(request.session.session_key),
                ).save()
            MyVerifCode.objects.filter(key=request.session.session_key).all().delete()
            MyLog.write_log(request.session.session_key, "ADMIN_2FA_GOBACK")
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.13 > Error in 2FA Goback Process.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red"]
        return True
    @staticmethod
    def twofactorauth_resend(request):
        if MyTime.check_last_time_from_log(request, "ADMIN_2FA_RESEND", 60) :
            request.session['status'] = ["Please wait before sending a code again.", "red"]
            return None
        MyLog.write_log(request.session.session_key, "ADMIN_2FA_RESEND")
        MyVerifCode.objects.filter(key=request.session.session_key).all().delete()
        jeton = MyRandom.get_random_number_str(9)
        enc_jeton = MyCrypto().sym_encrypt(jeton, "7RB3snJQy3p993AhN3F4a828PXuzpKgg")                
        if MyExternalRequest.telegram_send(jeton) != True:
            request.session['status'] = ["Can't send telegram message. Please contact us.", "red"]
            return None
        MyVerifCode(
            key = request.session.session_key, 
            code = enc_jeton,
            date = timezone.now()
        ).save()
        request.session['status'] = ["Message perfectly resend.", "green"]
        return True
    @staticmethod
    def clear_user_cache_information(request):
        try:
            MyVerifCode.objects.filter(key=request.session.session_key).all().delete()
            MyCaptcha.objects.filter(key=request.session.session_key).all().delete()
        except:
            pass
        return True
    @staticmethod
    def link_user_session(request, user_id, old_key):
        try:
            MyLinkBetweenUserAndSession(
                userid = str(user_id),
                status = str("LOGOUT"),
                old_key = str(old_key),
                new_key = str(request.session.session_key),
            ).save()
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.14 > Can't add data in MyLinkBetweenUserAndSession at logout.")
        return True