#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.conf import settings
from listings.system_language import MyLanguage
from listings.system_statistic import MyStatisticAction
from listings.system_security import MySecurity
from listings.system_log import MyLog
class Error(View):
    page_title = "Error"
    path = "error"
    template_rep = 'error.html'
    description_page = "An error occurred during your visit on the SDEV website. Contact us if the problem persists."
    def return_render(self, request, status = None):
        language = request.session.get('language', None)
        if language not in ['EN','FR', 'DE', 'ES', 'IT', 'PT'] or language == None or language == "":
            MyLanguage.get_most_appropriate_language(request)
        return render(
            request, 
            MyLanguage.get_view(request, self.template_rep),
            {   
                'status' : escape(status),
                'default_language' : escape(request.session['language']),
                'default_title' : f'LinkGarden > {escape(self.page_title)}',
                'description': escape(self.description_page),
            }
        )
    def get(self, request):
        MyStatisticAction.increment_trafic('get_trafic')
        if settings.DEVMODE:
            return redirect("/")
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        status = request.session.get('error', '200')
        try:
            del request.session['error']
        except:
            pass
        return self.return_render(request, status)
    def post(self, request):
        if settings.DEVMODE:
            return redirect("/")
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        if request.POST.get('paZLeWsrYNiZYtjP', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["paZLeWsrYNiZYtjP", "csrfmiddlewaretoken"],}) != True:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            if MySecurity.session_creation(request) != True:
                if MySecurity.verif_connection_banip(request):
                    return redirect("/")
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.81 > session_creation return False (But user is not banned).")
                return redirect(self.path)
            return redirect(self.path)
        elif request.POST.get('changelanguage', True) != True:
            if(MySecurity.verif_input(request.POST, {'input' : ["changelanguage", "csrfmiddlewaretoken"],}) != True):
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            if request.POST['changelanguage'] not in ['French', 'English', 'Spanish', 'Italian', 'Portuguese', 'German']:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            MyLanguage.change_current_language(request, request.POST['changelanguage'])
            return redirect(self.path)
        else:
            if MySecurity.update_score(request, "-", 50, self.path):
                return redirect("verification")