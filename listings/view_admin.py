#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from listings.models import MyRanking, MyContact
from listings.system_security import MySecurity
from listings.system_statistic import MyStatisticAction
from listings.system_external import MyExternalRequest
from listings.system_log import MyLog
class AdminDashboard(LoginRequiredMixin, PermissionRequiredMixin, View):
    path = "admin"
    permission_required = 'myuser.is_superuser'
    template_rep = "listings/admin/admin-dashboard.html"
    page_title = "Admin Dashboard"
    def return_render(self, request, sessstatus = None):
        if sessstatus != None and len(sessstatus) == 2:
            try:
                status = sessstatus[0]
                status_color = list(sessstatus)[1]
            except:
                status = ""
                status_color = ""
        else:
            status = ""
            status_color = ""

        data = []
        contact = []
        index = 1

        all_data = MyRanking.objects.filter(verified = False).values().order_by('-date')

        contact_data = MyContact.objects.all().values().order_by('-date')

        for x in all_data:
            data.append(
                {   
                    'index': escape(index),
                    'user_key': escape(x['user_key']),
                    'fname': escape(x['fname']),
                    'lname': escape(x['lname']),
                    'email': escape(x['email']),
                    'phone': escape(x['phone']),
                    'city': escape(x['city']),
                    'dep': escape(x['dep']),
                    'tarif': escape(x['tarif']),
                    'status': escape(x['status']),
                    'activity': escape(x['activity']),
                    'description': escape(x['description']),
                    'cvfiledata': escape(x['cvfiledata']),
                    'logofiledata': escape(x['logofiledata']),
                }
            )
            index += 1

        index = 0

        for y in contact_data:
            contact.append(
                {
                    'index':escape(index),
                    'name': escape(y['problem']),
                    'email': escape(y['email']),
                    'message': escape(y['message']),
                }
            )

        return render(
            request, 
            self.template_rep,
            {
                'status' : escape(status),
                'status_color': escape(status_color),
                'default_title' : f'LinkGarden > {escape(self.page_title)}',
                'data': data,
                'contact': contact,
            }
        )
    def get(self, request):
        try:
            del request.session['status']
        except:
            pass
        return self.return_render(request, sessstatus='status')
    def post(self, request):
        if request.session.get('ADMIN', False) == True and request.session.get('2FA', False) == True and request.user.is_authenticated:
            if MySecurity.verif_connection_banip(request):
                return MySecurity.kick_admin(request, "BAN IP - AdminDashboard - POST")
            if MySecurity.verif_session_shadowban(request):
                return MySecurity.kick_admin(request, "SHADOWBAN - AdminDashboard - POST")
            MySecurity.verif_session_flight(request)
            if MySecurity.verif_score(request, self.path):
                return MySecurity.kick_admin(request, "INSUFISANT SCORE - AdminDashboard - POST")
            if request.POST.get('action', True) != True and request.POST.get('user_key_action', True) != True  and request.POST.get('csrfmiddlewaretoken', True) != True:
                if request.POST['action'] not in ['valid', 'delete']:
                    return MySecurity.kick_admin(request, "INVALID ACTION DATA - AdminDashboard - POST")
                if MySecurity.clear_all_unexpected_space(request.POST['user_key_action']) == "":
                    return MySecurity.kick_admin(request, "INTERNAL ERROR #500 - AdminDashboard - POST")
                if request.POST['action'] == 'valid':
                    try:
                        MyRanking.objects.filter(user_key = request.POST['user_key_action']).update(verified = True)
                    except:
                        request.session['status'] = ['Erreur interne lors de la vérification du profile. Contactez le développeur.', 'red']
                        return redirect(self.path)
                else:
                    try:
                        MyRanking.objects.filter(user_key = request.POST['user_key_action']).delete()
                    except:
                        request.session['status'] = ['Erreur interne lors de la suppression du profile. Contactez le développeur.', 'red']
                        return redirect(self.path)
                request.session['status'] = ['Action réussite !', 'green']
                return redirect(self.path)
            else:
                return MySecurity.kick_admin(request, "INVALID_POST - AdminDashboard - POST")
        return redirect("/")