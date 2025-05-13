#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.contrib.auth import logout
from listings.backend_login import MyLoginAction
from listings.system_language import MyLanguage
from listings.system_captcha import MyCaptchaAction
from listings.system_security import MySecurity
from listings.system_statistic import MyStatisticAction
from listings.system_log import MyLog
class AdminLogin(View):
    path = "admin-login"
    page_title_1 = "Admin Login"
    page_title_2 = "2FA Login"
    first_page = "admin-login.html"
    sec_page = "admin-2FA.html"
    description_page = "LinkGarden Administrator login interface to access the LinkGarden admin area."
    def return_render(self, request, sessstatus = None, captcha = []):
        if sessstatus != None and len(sessstatus) == 3:
            try:
                status = sessstatus[0]
                status_color = sessstatus[1]
                reset_captcha = sessstatus[2]
            except:
                status = status_color = ""
                reset_captcha = False
        else:
            status = status_color =""
            reset_captcha = False
        language = request.session.get('language', None)
        if language not in ['EN','FR', 'DE', 'ES', 'IT', 'PT'] or language == None or language == "":
            MyLanguage.get_most_appropriate_language(request)
        if reset_captcha:
            captcha = MyCaptchaAction.reset_captcha(request)
        return render(
            request, 
            MyLanguage.get_view(request, self.first_page),
            {   
                'captcha' : captcha[1],
                'subject' : escape(MyLanguage.get_status_with_good_language(request.session['language'], captcha[0])),
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color' : escape(status_color),
                'default_language' : escape(language),
                'default_title' : f'LinkGarden > {escape(self.page_title_1)}',
                'description': escape(self.description_page),
            }
        )
    def return_second_page(self, request, sessstatus = None):
        if sessstatus != None:
            try:
                status = sessstatus[0]
                status_color = list(sessstatus)[1]
            except:
                status = status_color = ""
        else:
            status = status_color = ""
        language = request.session.get('language', None)
        if language not in ['EN','FR', 'DE', 'ES', 'IT', 'PT'] or language == None or language == "":
            MyLanguage.get_most_appropriate_language(request)
        return render(
            request, 
            MyLanguage.get_view(request, self.sec_page),
            {
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color': escape(status_color),
                'default_language' : escape(language),
                'default_title' : f'LinkGarden > {escape(self.page_title_2)}',
                'description': escape(self.description_page),
            }
        )
    def get(self, request):
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title_1)
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        if MySecurity.verif_session_shadowban(request):
            return redirect("/")
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        if request.session.get('2FA', False) == "WAIT_FOR_2FA_CODE":
            status = request.session.get('status', None)
            try:
                del request.session['status']
            except:
                pass
            return self.return_second_page(request, sessstatus=status)
        if request.session.get('2FA', False) == True and request.session.get('ADMIN', False) == True:
            return redirect('admin')
        captcha = MyCaptchaAction.get_captcha(request)
        status = request.session.get('status', None)
        try:
            del request.session['status']
        except:
            pass
        return self.return_render(request, status, captcha)
    def post(self, request):
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title_1)
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        if MySecurity.verif_session_shadowban(request):
            return redirect("/")
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        if request.POST.get('paZLeWsrYNiZYtjP', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["paZLeWsrYNiZYtjP", "csrfmiddlewaretoken"],}) != True:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
                return redirect(self.path)
            if MySecurity.session_creation(request) != True:
                if MySecurity.verif_connection_banip(request):
                    return redirect("/")
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.60 > session_creation return False (But user is not banned).")
                return redirect(self.path)
            return redirect(self.path)
        elif request.POST.get('changelanguage', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["changelanguage", "csrfmiddlewaretoken"],}) != True:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            if request.POST['changelanguage'] not in ['French', 'English', 'Spanish', 'Italian', 'Portuguese', 'German']:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            MyLanguage.change_current_language(request, request.POST['changelanguage'])
            return redirect(self.path)
        elif request.session.get('2FA', False) == True and request.session.get('ADMIN', False) == True:
            return redirect('admin')
        elif request.POST.get('username', True) != True and request.POST.get('password', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True and request.session.get('2FA', False) == False:
            if MyLoginAction.login_process(request) == False:
                return redirect("verification")
            return redirect(self.path)
        elif request.POST.get('c1', True) != True and request.POST.get('c2', True) != True and request.POST.get('c3', True) != True and request.POST.get('c4', True) != True and request.POST.get('c5', True) != True and request.POST.get('c6', True) != True and request.POST.get('c7', True) != True and request.POST.get('c8', True) != True and request.POST.get('c9', True) != True and request.session.get('2FA', False) == "WAIT_FOR_2FA_CODE" and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MyLoginAction.twofactorauth_process(request):
                return redirect("admin")
            return redirect(self.path)
        elif request.POST.get('back', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True and request.session.get('2FA', False) == "WAIT_FOR_2FA_CODE" and request.POST.get('csrfmiddlewaretoken', True) != True:
            MyLoginAction.twofactorauth_goback(request)
            return redirect(self.path)
        elif request.POST.get('resend', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True and request.session.get('2FA', False) == "WAIT_FOR_2FA_CODE" and request.POST.get('csrfmiddlewaretoken', True) != True:
            MyLoginAction.twofactorauth_resend(request)
            return redirect(self.path)
        else:
            if MySecurity.update_score(request, "-", 50, self.path):
                return redirect("verification")
def logout_user(request):
    MyStatisticAction.increment_trafic('get_trafic')
    if request.user.is_authenticated:
        MyLoginAction.clear_user_cache_information(request)
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
        MyLoginAction.link_user_session(request, user_id, old_key)
    return redirect('/')