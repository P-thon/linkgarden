#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.shortcuts import redirect
from listings.system_security import MySecurity
from listings.system_log import MyLog
from django.contrib.auth import logout
from listings.backend_login import MyLoginAction
def error400(request, exception=""):
    if MySecurity.update_score(request, "-", 30, "/"):
        if request.user.is_authenticated:
            MyLoginAction.clear_user_cache_information(request)
            MyLog.write_log(request.session.session_key, 'AUTO-LOGOUT-CSRF')
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
            return redirect("/")
        return redirect("verification")
    return redirect("/")
def error401(request, exception=""):
    if MySecurity.update_score(request, "-", 30, "/"):
        if request.user.is_authenticated:
            MyLoginAction.clear_user_cache_information(request)
            MyLog.write_log(request.session.session_key, 'AUTO-LOGOUT-CSRF')
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
            return redirect("/")
        return redirect("verification")
    return redirect("/")
def error403(request, reason = ""):
    if MySecurity.update_score(request, "-", 30, "/"):
        if request.user.is_authenticated:
            MyLoginAction.clear_user_cache_information(request)
            MyLog.write_log(request.session.session_key, 'AUTO-LOGOUT-CSRF')
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
            return redirect("/")
        return redirect("verification")
    return redirect("/")
def error404(request, exception):
    request.session['error'] = "404"
    MySecurity.update_score(request, "-", 10, "/")
    return redirect("error")
def error500(request):
    request.session['error'] = "500"
    MySecurity.update_score(request, "-", 10, "/")
    return redirect("error")
def error504(request, exception=""):
    request.session['error'] = "504"
    return redirect("error")
def errorcsrf(request, reason=""):
    if MySecurity.update_score(request, "-", 30, "/"):
        if request.user.is_authenticated:
            MyLoginAction.clear_user_cache_information(request)
            MyLog.write_log(request.session.session_key, 'AUTO-LOGOUT-CSRF')
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
            return redirect("/")
        return redirect("verification")
    return redirect("/")