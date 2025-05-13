#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import AppConfig
from django.core.exceptions import PermissionDenied, ViewDoesNotExist
from django.shortcuts import redirect

class MyAdminData(models.Model):
    key = models.fields.CharField(null=True, max_length=36)
    myfilter = models.fields.CharField(max_length=128, null = True)
    todo = models.fields.CharField(max_length=1024, null = True)
    link = models.fields.CharField(max_length=1024, null = True)
    link_description = models.fields.CharField(max_length=1024, null = True)
    chatgpt = models.fields.CharField(max_length=2048, null = True)
    chatgpt_status = models.fields.CharField(max_length=128, null = True)
    date = models.DateTimeField(null = True)

class MyUser(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    first_name = None
    last_name = None


class MyLinkBetweenUserAndSession(models.Model):
    userid = models.fields.CharField(null=True, max_length=255)
    status = models.fields.CharField(null=True, max_length=255)
    old_key = models.fields.CharField(null=True, max_length=255)
    new_key = models.fields.CharField(null=True, max_length=255)

class MyCaptcha(models.Model):
    key = models.fields.CharField(default = None,  max_length=255, primary_key=True)
    answer = models.fields.CharField(max_length=512, null = True)
    subject = models.fields.CharField(max_length=9, null = True)
    response = models.fields.CharField(max_length=9, null = True)
    date = models.DateTimeField(null = True)

class MyContact(models.Model):
    key = models.fields.CharField(max_length=255, null = True)
    email = models.fields.EmailField(null = True)
    problem = models.fields.CharField(max_length=64, null = True)
    message = models.fields.TextField(max_length=6048, null = True)
    warning = models.fields.BooleanField(null = True)
    date = models.DateTimeField(null = True)

class MyRanking(models.Model):
    user_key = models.fields.CharField(default = None, max_length=129, primary_key=True)
    key = models.fields.CharField(max_length=255, null = True)
    fname = models.fields.CharField(max_length=65, null = True)
    lname = models.fields.CharField(max_length=65, null = True)
    email = models.fields.EmailField(max_length=256, null = True)
    phone = models.fields.CharField(max_length=20, null = True)
    city = models.fields.CharField(max_length=65, null = True)
    dep = models.fields.CharField(max_length=65, null = True)
    status = models.fields.CharField(max_length=32, null = True)
    tarif = models.fields.CharField(max_length=16, null = True)
    activity = models.fields.CharField(max_length=32, null = True)
    description = models.fields.CharField(max_length=513, null = True)
    cvfiledata = models.FileField(upload_to = "pdf/", null = True, blank = True)
    logofiledata = models.ImageField(upload_to = "logo/", null = True, blank = True)
    verified = models.fields.BooleanField(default = False)
    ipaddress = models.fields.GenericIPAddressField(null = True, max_length = 32)
    date = models.DateTimeField(null = True)

class MyOpinion(models.Model):
    user_key = models.fields.CharField(max_length=129, null = True)
    note = models.fields.IntegerField(null = True)
    date = models.DateTimeField(null = True)

class MyTraficData(models.Model):
    get_trafic = models.fields.BigIntegerField(null = True)
    post_trafic = models.fields.BigIntegerField(null = True)
    total_trafic = models.fields.BigIntegerField(null = True)
    session_trafic = models.fields.BigIntegerField(null = True)
    ip_trafic = models.fields.BigIntegerField(null = True)
    referal_trafic = models.fields.BigIntegerField(null = True)
    direct_trafic = models.fields.BigIntegerField(null = True)
    browser_trafic = models.fields.BigIntegerField(null = True)
    date = models.DateTimeField(default = None, primary_key=True)

class MyIpBanList(models.Model):
    key = models.fields.CharField(null=True, max_length=36)
    ip = models.fields.CharField(default = None, max_length=255, primary_key=True)
    reason = models.fields.CharField(null=True, max_length=255)
    date_banned = models.DateTimeField(null = True)
    expiration_date = models.DateTimeField(null = True)

class MyIpManagement(models.Model):
    ip = models.fields.CharField(default = None, max_length=255, primary_key=True)
    score = models.fields.IntegerField(null=True)
    start_date = models.DateTimeField(null = True)
    last_request_date = models.DateTimeField(null = True)
    total_request_count = models.fields.BigIntegerField(null = True)

class MyStatisticData(models.Model):
    windows = models.fields.BigIntegerField(null = True)
    mac = models.fields.BigIntegerField(null = True)
    linux = models.fields.BigIntegerField(null = True)
    android = models.fields.BigIntegerField(null = True)
    ios = models.fields.BigIntegerField(null = True)
    other_os = models.fields.BigIntegerField(null = True)
    chrome = models.fields.BigIntegerField(null = True)
    firefox = models.fields.BigIntegerField(null = True)
    edge = models.fields.BigIntegerField(null = True)
    safari = models.fields.BigIntegerField(null = True)
    opera = models.fields.BigIntegerField(null = True)
    other_browser = models.fields.BigIntegerField(null = True)
    desktop = models.fields.BigIntegerField(null = True)
    tablet = models.fields.BigIntegerField(null = True)
    mobile = models.fields.BigIntegerField(null = True)
    from_referal = models.fields.BigIntegerField(null = True)
    from_direct = models.fields.BigIntegerField(null = True)
    from_browser = models.fields.BigIntegerField(null = True)
    total_get_trafic = models.fields.BigIntegerField(null = True)
    total_post_trafic = models.fields.BigIntegerField(null = True)
    total_session_trafic = models.fields.BigIntegerField(null = True)
    total_ip_trafic = models.fields.BigIntegerField(null = True)

class MySessionLog(models.Model):
    key = models.fields.CharField(default = None,  max_length=255)
    action = models.fields.CharField(max_length=512, null = True)
    date = models.DateTimeField(null = True)

class MyInternalError(models.Model):
    key = models.fields.CharField(default = None,  max_length=255)
    error = models.fields.CharField(max_length=512, null = True)
    date = models.DateTimeField(null = True)

class MyVerifCode(models.Model):
    key = models.fields.CharField(default = None,  max_length=255, primary_key=True)
    code = models.fields.CharField(max_length=512, null = True)
    date = models.DateTimeField(null = True)

class MyVisitor(models.Model):
    key = models.fields.CharField(default = None,  max_length=255, primary_key=True)
    os = models.fields.CharField(null = True, max_length=512)
    browser = models.fields.CharField(null = True, max_length=512)
    device = models.fields.CharField(null = True, max_length=512)
    language = models.fields.CharField(null = True, max_length=512)
    width = models.fields.IntegerField(null = True)
    height = models.fields.IntegerField(null = True)
    ip = models.fields.GenericIPAddressField(null = True, max_length=32)
    country = models.fields.CharField(null = True, max_length=512)
    city = models.fields.CharField(null = True, max_length=512)
    user_agent = models.fields.CharField(null = True, max_length=512)
    referer = models.fields.URLField(null = True)
    score = models.fields.IntegerField(null = True)
    fingerprint = models.fields.CharField(null = True, max_length=1000)
    date = models.DateTimeField(null = True)

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'
class PermissionDeniedErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            request.session['error'] = '403'
            return redirect('error')
        elif isinstance(exception, ViewDoesNotExist):
            request.session['error'] = '404'
            return redirect('error')
        return None