#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.utils.html import escape
from django.utils import timezone
from listings.models import MySessionLog, MyInternalError
from listings.system_external import MyExternalRequest
class MyLog:
    @staticmethod
    def write_log(key,action):
        try:
            MySessionLog(key=escape(key),action=escape(action),date=timezone.now()).save()
        except:
            return None
        return True
    @staticmethod
    def internal_error_log(key, error):
        if MyExternalRequest.send_notification(str(error)) == False:
            return None
        try:
            MyInternalError(
                key = escape(key),
                error = escape(error),
                date = timezone.now()
            ).save()
        except:
            return None
        return True
    @staticmethod
    def notif(message):
        if MyExternalRequest.send_notification(str(message)) == False:
            return None
        return True