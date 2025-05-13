#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com 
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers
from django.utils.html import escape
from listings.models import MyAdminData, MyVisitor
from django.utils import timezone
from listings.system_log import MyLog