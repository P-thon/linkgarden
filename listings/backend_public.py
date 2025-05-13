#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com 
import vaulty, base64
from django.utils import timezone
from django.utils.html import escape
from listings.models import MyIpBanList, MyCaptcha, MyRanking, MyOpinion, MyContact
from listings.system_captcha import MyCaptchaAction
from listings.system_security import MySecurity
from listings.system_default import MyTime, MyRandom
from listings.system_log import MyLog
class MyPublicAction():
    @staticmethod
    def register_form(request):
        if MyTime.check_last_time_from_log(request, "REGISTER_SUBMIT", 60):
            MyLog.write_log(request.session.session_key, "REGISTER_SUBMIT")
            if MySecurity.verif_spam_action(request, 'REGISTER_SUBMIT', 3, 1000):
                if MySecurity.update_score(request, "-", 50, "/"):
                    return None
                return None
            request.session['status'] = ["Please wait 60s before trying again.", "red"]
            return False
        MyLog.write_log(request.session.session_key, "REGISTER_SUBMIT")
        if MySecurity.verif_spam_action(request, 'REGISTER_SUBMIT', 5, 3600):
            if MySecurity.update_score(request, "-", 50, "/"):
                return None
            return None
        invalid = False
        if len(request.POST) + 1 != len(['fname', 'lname', 'email', 'phone', 'city', 'dep', 'status', 'tarif', 'work', 'desc', 'cvfile', 'logofile', 'csrfmiddlewaretoken']):
            invalid = True
        for x in ['fname', 'lname', 'email', 'phone', 'city', 'dep', 'status', 'tarif', 'work', 'desc', 'csrfmiddlewaretoken']:
            try:
                if MySecurity.is_string_empty(request.POST[x]):
                    invalid = True
                    break
            except:
                invalid = True
                break
        try:
            cv_data = request.FILES['cvfile']
        except:
            invalid = True
        try:
            logo_data = request.FILES['logofile']
        except:
            invalid = True
        if invalid:
            if MySecurity.update_score(request, "-", 50, "register"):
                return None
        if MySecurity.verif_name(request.POST['fname']) != True  or len(request.POST['fname']) > 64:
            request.session['status'] = ["Invalid firstname.", "red"]
            return False
        if MySecurity.verif_name(request.POST['lname']) != True or len(request.POST['lname']) > 64:
            request.session['status'] = ["Invalid lastname.", "red"]
            return False
        if MySecurity.verif_email(request.POST['email']) != True or len(request.POST['email']) > 255:
            request.session['status'] = ["Invalid email.", "red"]
            return False
        if MySecurity.verif_name(request.POST['city']) != True or len(request.POST['city']) > 64:
            request.session['status'] = ["Invalid city.", "red"]
            return False
        if MySecurity.verif_name(request.POST['dep']) != True or len(request.POST['dep']) > 64:
            request.session['status'] = ["Invalid department.", "red"]
            return False
        if len(request.POST['phone']) > 18:
            request.session['status'] = ["Invalid phone number.", "red"]
            return False
        if request.POST['work'] not in ['jardinier', 'paysagiste', 'pisciniste', 'elagueur', "swork", "nhp", "other"]:
            request.session['status'] = ["Invalid work selection.", "red"]
            return False
        if request.POST['status'] not in ['particulier', 'entreprise']:
            request.session['status'] = ["Invalid work selection.", "red"]
            return False
        if len(request.POST['desc']) >= 512 or '<form>' in request.POST['desc'] or '</form>' in request.POST['desc'] or  '<script>' in request.POST['desc'] or '</script>' in request.POST['desc'] or 'INSERT INTO' in request.POST['desc'] or 'SELECT * FROM' in request.POST['desc']:
            request.session['status'] = ["Invalid description.", "red"]
            return False
        if cv_data.size >= 100000001:
            request.session['status'] = ["Invalid CV file size. Less than 1Mo please.", "red"]
            return False
        if len(cv_data.name) >= 65:
            request.session['status'] = ["Invalid CV filename.", "red"]
            return False
        if cv_data.name[-4:].lower() not in ['.pdf', '.jpg', '.png', 'jpeg']:
            request.session['status'] = ["Invalid CV file extension.", "red"]
            return False
        if cv_data.content_type not in ["application/pdf", "image/jpeg", "image/jpg", "image/png"]:
            request.session['status'] = ["Invalid CV file extension.", "red"]
            return False
        if logo_data.size >= 100000001:
            request.session['status'] = ["Invalid LOGO file size. Less than 1Mo please.", "red"]
            return False
        if len(logo_data.name) >= 65:
            request.session['status'] = ["Invalid LOGO filename.", "red"]
            return False
        if logo_data.name[-4:].lower() not in ['.pdf', '.jpg', '.png', 'jpeg']:
            request.session['status'] = ["Invalid LOGO file extension.", "red"]
            return False
        if logo_data.content_type not in ["application/pdf", "image/jpeg", "image/jpg", "image/png"]:
            request.session['status'] = ["Invalid LOGO file extension.", "red"]
            return False
        if request.POST['tarif'] not in ["5to20", "20to40", "40to60", "60to80", "80to100", "100tomore"]:
            request.session['status'] = ["Invalid tarif.", "red"]
            return False

        ext1 = cv_data.name[-4:].lower()
        ext2 = logo_data.name[-4:].lower()
        uk = MyRandom.get_random_string(128)
        cv_data.name = uk + ext1
        logo_data.name = uk + ext2
        
        # try:
        MyRanking(
            user_key = uk,
            key = request.session.session_key,
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            city = request.POST['city'],
            dep = request.POST['dep'],
            tarif = request.POST['tarif'],
            status = request.POST['status'],
            activity = request.POST['work'],
            description = request.POST['desc'],
            cvfiledata = cv_data,
            logofiledata = logo_data,
            ipaddress = MySecurity.get_ip(request),
            verified = False,
            date = timezone.now()
        ).save()
        # except:
        #     print("ERROR")
        #     MyLog.internal_error_log(request.session.session_key, "Internal Error 1.20 > My Insert Error in apply proccess.")
        #     request.session['status'] = ["Internal Error 500. We have been notified. Try again.", "red"]
        #     return False

        MyLog.notif("Une personne à postuler.")

        request.session['status'] = ["Your application has been processed. We will contact you by email.", "green"]

        return True
    @staticmethod
    def contact_form(request):
        print('aaaaa')
        warn = False
        if MySecurity.verif_session_shadowban(request):
            warn = True
        if MyTime.check_last_time_from_log(request, "CONTACT_SUBMIT", 30):
            MyLog.write_log(request.session.session_key, "CONTACT_SUBMIT")
            if MySecurity.verif_spam_action(request, 'CONTACT_SUBMIT', 3, 1000):
                if MySecurity.update_score(request, "-", 50, "contact"):
                    return None
                return None
            request.session['status'] = ["Please wait 30s before trying again.", "red"]
            return False
        MyLog.write_log(request.session.session_key, "CONTACT_SUBMIT")
        if MySecurity.verif_spam_action(request, 'CONTACT_SUBMIT', 3, 1000):
            if MySecurity.update_score(request, "-", 50, "contact"):
                return None
            return None
        if MySecurity.verif_input(request.POST, {'input' : ["name", "email", "message", "csrfmiddlewaretoken"],}) != True:
            if MySecurity.update_score(request, "-", 50, "contact"):
                return None
        if MySecurity.verif_email(request.POST['email']) == False:
            request.session['status'] = ["Invalid email.", "red"]
            return False
        if len(request.POST['message']) >= 2049:
            request.session['status'] = ["Your message is too long.", "red"]
            return False        
        if '<script>' in request.POST['message'] or '<form>' in request.POST['message'] or 'INSERT INTO' in request.POST['message'] or 'SELECT *' in request.POST['message']:
            warn = request.session['SHADOWBAN'] = True
        try:
            MyContact(
                key = request.session.session_key,
                email = escape(request.POST['email']),
                problem = escape(request.POST['name']),
                message = escape(request.POST['message']),
                warning = warn,
                date = timezone.now()
            ).save()
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.21 > MyContact Insert Error in apply proccess.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red"]
            return False
        request.session['status'] = ["Your message has been sent to us. We will contact you soon.", "green"]
        print("good")
        return True

    @staticmethod
    def verification_form(request, path):
        if request.POST['verification'] != "k4Rf36vNW46zWcR2":
            MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid post data.", str(timezone.now() + timezone.timedelta(seconds=3600)))
            return None
        if MyTime.check_last_time_from_log(request, "VERIFICATION_BOT_SUBMIT", 10):
            MyLog.write_log(request.session.session_key, "VERIFICATION_BOT_SUBMIT")
            if MySecurity.verif_spam_action(request, 'VERIFICATION_BOT_SUBMIT', 5, 180):
                MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid captcha submit.", str(timezone.now() + timezone.timedelta(seconds=3600)))
                return None
            request.session['status'] = ["Please wait 10s before trying again.", "red", False]
            return False
        MyLog.write_log(request.session.session_key, "VERIFICATION_BOT_SUBMIT")
        if MySecurity.verif_spam_action(request, 'VERIFICATION_BOT_SUBMIT', 5, 180):
            MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid captcha submit.", str(timezone.now() + timezone.timedelta(seconds=3600)))
            return None
        status = MyCaptchaAction.verif_captcha(request)
        if status is None:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.24 > Can't verif catptcha.")
            request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            return False
        if status == False:
            return False
        MyLog.write_log(request.session.session_key, 'BOT_VERIFICATION_GOOD')
        MySecurity.update_score(request, "+", 50, path)
        try:
            MyIpBanList.objects.filter(ip = MySecurity.get_ip(request)).all().delete()
            MyCaptcha.objects.filter(key=request.session.session_key).all().delete()
        except:
            pass
        if request.session.get('BEFORE_PATH', False) != False:
            try:
                return request.session['BEFORE_PATH']
            except:
                return None
        else:
            return None
        
    @staticmethod
    def add_opinion_form(request):
        # Vérifier si la clef est valide.
        if MyTime.check_last_time_from_log(request, "OPINION_SUBMIT", 300):
            MyLog.write_log(request.session.session_key, "OPINION_SUBMIT")
            if MySecurity.verif_spam_action(request, 'OPINION_SUBMIT', 5, 3600):
                if MySecurity.update_score(request, "-", 50, "/"):
                    return None
                return None
            request.session['status'] = ["Please wait 300s before adding a mark again.", "red"]
            return False
        MyLog.write_log(request.session.session_key, "OPINION_SUBMIT")
        if MySecurity.verif_spam_action(request, 'OPINION_SUBMIT', 5, 3600):
            if MySecurity.update_score(request, "-", 50, "/"):
                return None
            return None

        if MyRanking.objects.filter(user_key = request.POST['userid']).count() == 0:
            if MySecurity.update_score(request, "-", 50, "/"):
                return None
        try:
            note = int(request.POST['addopinion'])
            if 0 <= note <= 5:
                MyOpinion(
                    user_key = request.POST['userid'],
                    note = note,
                    date = timezone.now()
                ).save()
            else:
                if MySecurity.update_score(request, "-", 50, "/"):
                    return None
        except:
            if MySecurity.update_score(request, "-", 50, "/"):
                return None
            return None
        return True