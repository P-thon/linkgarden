#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.utils import timezone
from django.conf import settings
from listings.backend_public import MyPublicAction
from listings.system_captcha import MyCaptchaAction
from listings.system_language import MyLanguage
from listings.system_statistic import MyStatisticAction
from listings.system_security import MySecurity
from listings.system_log import MyLog
from listings.models import MyRanking, MyOpinion
class Home(View):
    page_title = "Home"
    path = "/"
    template_rep = 'home.html'
    description_page = "Welcome on the LinkGarden website."
    def return_render(self, request, sessstatus = None):
        if sessstatus != None and len(sessstatus) == 2:
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
            MyLanguage.get_view(request, self.template_rep),
            {
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color': escape(status_color),
                'default_language' : escape(request.session['language']),
                'default_title' : f'LinkGarden > {escape(self.page_title)}',
                'description': escape(self.description_page),
            }
        )
    def return_render_devmode(self, request, sessstatus = None):
        if sessstatus != None and len(sessstatus) == 2:
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
            MyLanguage.get_view(request, 'devmode.html'),
            {   
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color': escape(status_color),
                'default_language' : escape(language),
                'default_title' : 'LinkGarden > Soon',
                'description': escape(self.description_page),
            }
        )
    def get(self, request):
        MyStatisticAction.increment_trafic('get_trafic')
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
            return MySecurity.get_ban(request, 'Ban')
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        status = request.session.get('status', None)
        try:
            del request.session['status']
        except:
            pass
        if settings.DEVMODE:
            return self.return_render_devmode(request, status)
        return self.return_render(request, status)
    def post(self, request):
        MyStatisticAction.increment_trafic('post_trafic')
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
            if request.POST.get('paZLeWsrYNiZYtjP', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
                if MySecurity.verif_input(request.POST, {'input' : ["paZLeWsrYNiZYtjP", "csrfmiddlewaretoken"],}) != True:
                    if MySecurity.update_score(request, "-", 50, self.path):
                        return redirect("verification")
                    return redirect(self.path)
                if MySecurity.session_creation(request) != True:
                    MyLog.internal_error_log(request.session.session_key, "Internal Error 1.73 > session_creation return False (But user is not banned).")
                    return redirect(self.path)
                request.session['status'] = "9wgJ2Svy8eazG4Vv35D58gb36EFLJxB2"
                return redirect(self.path)
            elif request.POST.get('6y4he2WjST893zT7tbsaPK2A39WTW7cs', True) != True:
                if request.POST['6y4he2WjST893zT7tbsaPK2A39WTW7cs'] == "y64j38zT9hST27eW3tsa9WbP2ATcKs7W":
                    MySecurity.manual_unbanip(request, MySecurity.get_ip(request))
                    return redirect(self.path)
            return redirect(self.path)
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        if request.POST.get('paZLeWsrYNiZYtjP', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["paZLeWsrYNiZYtjP", "csrfmiddlewaretoken"],}) != True:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
                return redirect(self.path)
            if MySecurity.session_creation(request) != True:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.74 > session_creation return False (But user is not banned).")
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
        elif request.POST.get('name', True) != True and request.POST.get('email', True) != True and request.POST.get('message', True) != True:
            if MyPublicAction.contact_form(request) is None:
                return redirect("verification")
            return redirect(self.path)
        else:
            if MySecurity.update_score(request, "-", 50, self.path):
                return redirect("verification")

class Register(View):
    page_title = "Register"
    path = "register"
    template_rep = 'register.html'
    description_page = ""
    def return_render(self, request, sessstatus = ""):
        if sessstatus != None and len(sessstatus) == 2:
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
            MyLanguage.get_view(request, self.template_rep),
            {
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color': escape(status_color),
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
        status = request.session.get('status', None)
        try:
            del request.session['status']
        except:
            pass
        return self.return_render(request, status)
    def post(self, request):
        MyStatisticAction.increment_trafic('post_trafic')
        if settings.DEVMODE:
            return redirect("/")
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
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
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.71 > session_creation return False (But user is not banned).")
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

        elif request.POST.get('fname', True) != True and request.POST.get('lname', True) != True and request.POST.get('email', True) != True and request.POST.get('phone', True) != True and request.POST.get('city', True) != True and request.POST.get('dep', True) != True and request.POST.get('status', True) != True and request.POST.get('tarif', True) != True and request.POST.get('work', True) != True and request.POST.get('desc', True) != True and request.FILES.get('cvfile', True) != True and request.FILES.get('logofile', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:

            if MyPublicAction.register_form(request) is None:
    
                return redirect("verification")
 
            return redirect(self.path)

        else:

            if MySecurity.update_score(request, "-", 50, self.path):
    
                return redirect("verification")

            return redirect(self.path)


class Verification(View):
    page_title = "Verification"
    path = "verification"
    template_rep = 'verification.html'
    description_page = "Suspicious activity has been detected during your visit to the LinkGarden site. Fill in this captcha to continue browsing."
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
            MyLanguage.get_view(request, self.template_rep),
            {   
                'captcha' : captcha[1],
                'subject' : escape(MyLanguage.get_status_with_good_language(request.session['language'], captcha[0])),
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color' : escape(status_color),
                'default_language' : escape(language),
                'default_title' : f'LinkGarden > {escape(self.page_title)}',
                'description': escape(self.description_page),
            }
        )
    def get(self, request):
        try:
            del request.session['status']
        except:
            pass
        return self.return_render(request, 'status', 'captcha')
    def post(self, request):
        MyStatisticAction.increment_trafic('post_trafic')
        if request.POST.get('6y4he2WjST893zT7tbsaPK2A39WTW7cs', True) != True:
            if request.POST['6y4he2WjST893zT7tbsaPK2A39WTW7cs'] == "y64j38zT9hST27eW3tsa9WbP2ATcKs7W":
                MySecurity.manual_unbanip(request, MySecurity.get_ip(request))
                return redirect("admin-login")
            else:
                MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid post data.", str(timezone.now() + timezone.timedelta(seconds=3600)))
                return redirect("/")
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        try:
            if request.session['SCORE'] > settings.MINIMUM_SCORE:
                return redirect("/")
        except:
            return redirect("/")
        if request.POST.get('changelanguage', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["changelanguage", "csrfmiddlewaretoken"],}) != True:
                MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid post data.", str(timezone.now() + timezone.timedelta(seconds=3600)))
                return redirect("/")
            if request.POST['changelanguage'] not in ['French', 'English', 'Spanish', 'Italian', 'Portuguese', 'German']:
                MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid post data.", str(timezone.now() + timezone.timedelta(seconds=3600)))
                return redirect("/")
            MyLanguage.change_current_language(request, request.POST['changelanguage'])
            return redirect(self.path)
        elif request.POST.get('verification', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            data = MyPublicAction.verification_form(request, self.path)
            if data is None:
                return redirect("/")
            elif data == False:
                return redirect(self.path)
            else:
                if data not in settings.PATH_LIST:
                    return redirect("/")
                return redirect(data)
        else:
            MySecurity.add_banip(request, MySecurity.get_ip(request), "Too much invalid post data.", str(timezone.now() + timezone.timedelta(seconds=3600)))
            return redirect("/")

class Ranking(View):
    page_title = "Ranking"
    path = "ranking"
    template_rep = 'ranking.html'
    description_page = "Ranking system make by Link Garden to improve customer choice."
    def return_render(self, request, sessstatus = None):
        if sessstatus != None and len(sessstatus) == 2:
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

        data = []
        index = 1

        all_data = MyRanking.objects.filter(verified = True).values().order_by('-date')

        for x in all_data:
            
            note = []
            
            opinion = MyOpinion.objects.filter(user_key = x['user_key']).values("note").all()

            for y in opinion:
    
                note.append(int(y['note']))
            
            try:
                final = round((sum(note) / len(note)) * 2) / 2
                if final > 5:
                    final = 5
                elif final < 0:
                    final = 0
            except:
                final = 0

            data.append(
                {
                    'user_key': escape(x['user_key']),
                    'fname': escape(x['fname']),
                    'lname': escape(x['lname']),
                    'email': escape(x['email']),
                    'phone': escape(x['phone']),
                    'city': escape(x['city']),
                    'dep': escape(x['dep']),
                    'status': escape(x['status']),
                    'tarif': escape(x['tarif']),
                    'activity': escape(x['activity']),
                    'description': escape(x['description']),
                    'cvfiledata': escape(x['cvfiledata']),
                    'logofiledata': escape(x['logofiledata']),
                    'note': final,
                    'len_note': MyOpinion.objects.filter(user_key = x['user_key']).values("note").count(),
                }
            )

        dec_data = MySecurity.tri_decroissant(data)

        for x in dec_data:
            x['index'] = index
            index += 1

        return render(
            request, 
            MyLanguage.get_view(request, self.template_rep),
            {
                'status' : escape(MyLanguage.get_status_with_good_language(request.session['language'], status)),
                'status_color': escape(status_color),
                'data': dec_data,
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
        status = request.session.get('status', None)
        try:
            del request.session['status']
        except:
            pass
        return self.return_render(request, status)
    def post(self, request):
        MyStatisticAction.increment_trafic('post_trafic')
        if settings.DEVMODE:
            return redirect("/")
        if MySecurity.verif_session_exist(request):
            return MySecurity.post_antispam(request, self.page_title)
        if MySecurity.verif_connection_banip(request):
            return redirect("/")
        MySecurity.verif_session_flight(request)
        if MySecurity.verif_score(request, self.path):
            return redirect("verification")
        if request.POST.get('paZLeWsrYNiZYtjP', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MySecurity.verif_input(request.POST, {'input' : ["paZLeWsrYNiZYtjP", "csrfmiddlewaretoken"],}) != True:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            if MySecurity.session_creation(request) != True:
                if MySecurity.verif_connection_banip(request):
                    return redirect("/")
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.82 > session_creation return False (But user is not banned).")
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
        elif request.POST.get('addopinion', True) != True and request.POST.get('userid', True) != True and request.POST.get('csrfmiddlewaretoken', True) != True:
            if MyPublicAction.add_opinion_form(request) is None:
                if MySecurity.update_score(request, "-", 50, self.path):
                    return redirect("verification")
            return redirect(self.path)
        else:
            if MySecurity.update_score(request, "-", 50, self.path):
                return redirect("verification")
            