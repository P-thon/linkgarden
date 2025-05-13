#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
import base64, re, json, geocoder, difflib, PyPDF2
from datetime import datetime
from user_agents import parse
from geopy.geocoders import Nominatim
from django.conf import settings
from django.utils import timezone
from django.utils.html import escape
from django.shortcuts import render, redirect
from listings.system_log import MyLog
from listings.models import MyIpBanList, MyVisitor, MySessionLog, MyIpManagement
from listings.system_statistic import MyStatisticAction
from listings.system_default import MyTime
class MySecurity:
    @staticmethod
    def session_creation(request):
        MyLog.write_log(request.session.session_key, 'FIRST_CONNECTION')
        MyStatisticAction.increment_trafic("session_trafic")
        request.session['SCORE'] = 0
        request.session['SHADOW'] = False
        request.session['FULLBAN'] = False
        request.session['ADMIN'] = False
        request.session['2FA'] = False
        request.session['CURRENT_HEADER'] = request.headers['User-Agent']
        request.session['CURRENT_IP'] = MySecurity.get_ip(request)
        if MyIpManagement.objects.filter(ip=MySecurity.get_ip(request)).values().count() == 0:
            data = MySecurity.clear_data_and_generate_score(request)
            request.session['SCORE'] = data['score']
            if MyStatisticAction.update_statistic(request, data) != True:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.40 > MyStaticData Update Error in session_creation.")
                request.session['status'] = ["Internal Error 500. We have been notified.", "red", False]
            try:
                MyIpManagement(
                    ip = MySecurity.get_ip(request),
                    score = data['score'],
                    start_date = str(timezone.now()),
                    last_request_date = str(timezone.now()),
                    total_request_count = 2,
                ).save()
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.41 > MyIpManagement Insert Error in session_creation.")
            try:
                MyVisitor(
                    key = request.session.session_key, 
                    os = data["user_os"],
                    browser = data["user_browser"],
                    user_agent = data["user_agent"],
                    device = data["user_device"],
                    language = data["user_language"].upper(),
                    width = data["user_width"],
                    height = data["user_height"],
                    ip = data["user_ip"],
                    referer = data["user_referer"],
                    country = data["user_country"],
                    city = data["user_city"],
                    score = data["score"],
                    fingerprint = str(base64.b64encode(str(data).encode("utf-8"))),
                    date = timezone.now()
                ).save()
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.42 > MyVisitor Insert Error in session_creation.")
            return True
        else:
            profile = MySecurity.get_ip_profile(request)   
            data = MySecurity.clear_data_and_generate_score(request)
            if MyTime.time_checker(profile['last_request_date'], 86400)  != True:
                request.session['SCORE'] = data['score']
                try:
                    MyIpManagement(
                        ip = MySecurity.get_ip(request),
                        score = data['score'],
                        start_date = str(timezone.now()),
                        last_request_date = str(timezone.now()),
                        total_request_count = 2,
                    ).save()
                except:
                    MyLog.internal_error_log(request.session.session_key, "Internal Error 1.43 > MyIpManagement Update Error in session_creation.")
            else:
                request.session['SCORE'] = profile['score']
            if MyStatisticAction.update_statistic(request, data) != True:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.44 > MyStatisticData Update Error in session_creation.")
            try:
                MyVisitor(
                    key = request.session.session_key, 
                    os = data["user_os"],
                    browser = data["user_browser"],
                    user_agent = data["user_agent"],
                    device = data["user_device"],
                    language = data["user_language"].upper(),
                    width = data["user_width"],
                    height = data["user_height"],
                    ip = data["user_ip"],
                    referer = data["user_referer"],
                    country = data["user_country"],
                    city = data["user_city"],
                    score = data["score"],
                    fingerprint = str(base64.b64encode(str(data).encode("utf-8"))),
                    date = timezone.now()
                ).save()
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.45 > MyVisitor Insert Error in session_creation.")
            return True
    @staticmethod
    def get_ip_profile(request):
        user_data = MyIpManagement.objects.filter(ip = MySecurity.get_ip(request)).values()[:1].get()
        return user_data
    @staticmethod
    def update_user_trafic(request):
        user_ip = MySecurity.get_ip(request)
        user_data = MySecurity.get_ip_profile(request)
        try:
            MyIpManagement.objects.filter(ip = user_ip).update(total_request_count = int(user_data["total_request_count"]) + 1, last_request_date = str(timezone.now()))
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.46 > MyIpManagement Update Error in session_creation.")
            return None
        return True
    @staticmethod
    def update_user_score(request, new_score):
        user_ip = MySecurity.get_ip(request)
        try:
            MyIpManagement.objects.filter(ip = user_ip).update(score = new_score)
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.47 > MyIpManagement Update Error when updating score.")
            return None
        return True
    @staticmethod
    def verif_ip_trafic(request):
        return True
    @staticmethod
    def add_banip(request, ip : str, reason : str, expiration_date):
        request.session['FULLBAN'] = True
        request.session['FULLBANTIME'] = str(timezone.now())
        request.session['status'] = [str(reason), "red"]
        try:
            MyIpBanList(
                key = request.session.session_key,
                ip = ip,
                date_banned = str(timezone.now()),
                reason = reason,
                expiration_date = expiration_date,
            ).save()
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.48 > MyIpBanList Insert Error.")
            return None
        return True
    @staticmethod
    def verif_connection_banip(request):
        ip = MySecurity.get_ip(request)
        if request.session.get('FULLBAN', False) != False:
            try:
                data = MyIpBanList.objects.filter(ip = ip).values("expiration_date").all()[:1][0]
            except:
                request.session['FULLBAN'] = False
                return False
            expire = datetime.strptime(str(data['expiration_date']), '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
            if expire <= now:
                try:
                    MyIpBanList.objects.filter(ip=ip).all().delete()[:1]
                    MySecurity.update_score(request, "+", 100, "/")
                except:
                    MyLog.internal_error_log(request.session.session_key, "Internal Error 1.49 > MyIpBanList / MyIpManagement Delete Error.")
                    return True
                return False
            return True
        if MyIpBanList.objects.filter(ip=ip).values().count() != 0:
            try:
                data = MyIpBanList.objects.filter(ip = ip).values("expiration_date").all()[:1][0]
            except:
                request.session['FULLBAN'] = False
                return False
            expire = datetime.strptime(str(data['expiration_date']), '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
            if expire <= now:
                try:
                    MyIpBanList.objects.filter(ip=ip).all().delete()[:1]
                    MySecurity.update_score(request, "+", 100, "/")
                except:
                    MyLog.internal_error_log(request.session.session_key, "Internal Error 1.50 > MyIpBanList / MyIpManagement Delete Error.")
                    return True
                return False
            request.session['FULLBAN'] = True
            return True
        return False
    @staticmethod
    def manual_unbanip(request, ip):
        if request.user.is_authenticated:
            try:
                MyIpBanList.objects.filter(ip=ip).all().delete()[:1]
                MySecurity.update_score(request, "+", 100, "/")
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.51 > MyIpBanList / MyIpManagement Delete Error.")
                return False
            try:
                del request.session['status']
            except:
                pass
            MyLog.write_log(request.session.session_key, f"USER_{request.user.id}_UNBAN_{escape(ip)}")
            return True
        else:
            try:
                MyIpBanList.objects.filter(ip=ip).all().delete()[:1]
                MySecurity.update_score(request, "+", 100, "/")
                request.session['SCORE'] = 100
                request.session['SHADOW'] = False
                request.session['FULLBAN'] = False
                request.session['ADMIN'] = False
                request.session['2FA'] = False
                request.session['CURRENT_HEADER'] = request.headers['User-Agent']
                request.session['CURRENT_IP'] = MySecurity.get_ip(request)
                try:
                    del request.session['status']
                except:
                    pass
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.52 > MyIpBanList / MyIpManagement Delete Error.")
                return False
            MyLog.notif(f"{escape(ip)} USE BACKDOOR TO UNBAN HIMSELF.")
            return True
    @staticmethod 
    def update_score(request, sign : str, value : int, current_path : str) -> int:
        request.session['BEFORE_PATH'] = current_path 
        return False
        # score = request.session.get('SCORE', 0)
        # if sign == "+":
        #     if (score + value) > 100:
        #         score = 100
        #     else:
        #         score += value
        # elif sign == "-":
        #     if (score - value) < 0:
        #         score = 0
        #     else:
        #         score -= value
        # request.session['SCORE'] = score
        # MySecurity.update_user_score(request, score)
        # if score <= settings.MINIMUM_SCORE:
        #     MyLog.write_log(request.session.session_key, 'BOT_VERIFICATION_ASKED')
        #     request.session['SHADOW'] = True
        #     request.session['BEFORE_PATH'] = current_path 
        #     return True
        # else:
        #     return False
    @staticmethod
    def clear_data_and_generate_score(request):
        score = 0
        try:
            header = dict(request.headers)
            user_data = escape(request.POST['paZLeWsrYNiZYtjP'])
            decrypt_data = base64.b64decode(user_data).decode('utf-8')
            client = json.loads(decrypt_data)
        except:
            return None
        if len(client) != 15:
            return None
        for x in client:
            if x not in ['sw', 'sh', 'cd', 'pd', 'hl', 'ce', 'la', 'ua', 'on', 'pv', 'hc', 'wd', 'ab', 'nw', 'dm'] or x == "" or x == None:
                return None
            if x == "sw":
                try:
                    user_width = int(client[x])
                    if user_width <= 0 or user_width >= 30000:
                        score -= 2
                        user_width = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_width = None
                    continue
            elif x == "sh":
                try:
                    user_height = int(client[x])
                    if user_height <= 0 or user_height >= 30000:
                        score -= 2
                        user_height = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_height = None
                    continue
            elif x == "cd":
                try:
                    user_colordepth = int(client[x])
                    if user_colordepth <= 0 or user_colordepth >= 30000:
                        score -= 2
                        user_colordepth = None
                        continue
                    score += 2
                except:
                    score -= 2
                    user_colordepth = None
                    continue
            elif x == "pd":
                try:
                    user_pixeldepth = int(client[x])
                    if user_pixeldepth <= 0 or user_pixeldepth >= 30000:
                        score -= 2
                        user_pixeldepth = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_pixeldepth = None
                    continue
            elif x == "hl":
                try:
                    user_historylength = int(client[x])
                    if user_historylength <= 0 or user_historylength >= 30000:
                        score -= 2
                        user_historylength = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_historylength = None
                    continue
            elif x == "ce":
                try:
                    user_cookieok = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_cookieok = None
                    continue
            elif x == "la":
                try:
                    user_language = escape(str(client[x]))
                    if re.search(re.compile('[0-9.<.>./.?.;.=.+.-.|.".*.$.!.:]'), user_language) or len(user_language) > 8:
                        score -= 2
                        user_language = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_language = None
                    continue
            elif x == "ua":
                try:
                    user_agent = escape(str(client[x]))
                    score += 3
                except:
                    score -= 2
                    user_agent = None
                    continue
            elif x == "on":
                try:
                    user_navok = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_navok = None
                    continue
            elif x == "pv":
                try:
                    user_pdfok = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_pdfok = None
                    continue
            elif x == "hc":
                try:
                    user_hardware = int(client[x])
                    if user_hardware <= 0 or user_hardware >= 30000:
                        score -= 2
                        user_hardware = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_hardware = None
                    continue
            elif x == "wd":
                try:
                    user_webdriverok = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_webdriverok = None
                    continue
            elif x == "ab":
                try:
                    user_adblocker = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_adblocker = None
                    continue
            elif x == "nw":
                try:
                    user_joining = int(client[x])
                    if user_joining <= 0 or user_joining >= 1000000000000000000000000000000000000000:
                        score -= 2
                        user_joining = None
                        continue
                    score += 3
                except:
                    score -= 2
                    user_joining = None
                    continue
            elif x == "dm":
                try:
                    user_darkmode = bool(client[x])
                    score += 3
                except:
                    score -= 2
                    user_darkmode = None
                    continue
        ua = parse(user_agent)
        user_browser = ua.browser.family
        user_os = ua.os.family
        if ua.is_bot:
            score -= 30
        elif ua.is_mobile:
            user_device = "Mobile"
        elif ua.is_tablet:
            user_device = "Tablet"
        elif ua.is_pc:
            user_device = "Desktop"
        else:
            user_device = None
        score += 5
        user_ip = MySecurity.get_ip(request)
        try:
            gps_co = geocoder.ip(user_ip).latlng
            if gps_co is None:
                user_country = None
                user_city = None
            else :
                geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0")
                location = geolocator.reverse(str(gps_co[0])+","+str(gps_co[1]))
                address = location.raw['address']
                user_city = escape(address.get('city', ''))
                user_town = escape(address.get('town', ''))
                user_village = escape(address.get('village', ''))
                user_country = escape(address.get('country', ''))
                if user_city != "" or len(user_city) != 0:
                    user_city = user_city
                elif user_town != "" or len(user_town) != 0 :
                    user_city = user_town
                elif user_village != "" or len(user_village) != 0:
                    user_city = user_village
                else:
                    user_city = None
        except:
            user_country = None
            user_city = None
        score += 5
        try:
            user_referer = request.META['HTTP_REFERER']
            score += 5
        except:
            user_referer = None
        score += 20
        if ua.device.family == "Other":
            user_os = ua.os.family
        else:
            user_os = ua.os.family + " > " + ua.device.family
            score += 5
        for x in header:
            if x in ['Content-Length','Content-Type','Host','User-Agent','Accept','Accept-Language','Accept-Encoding','Origin','Dnt','Connection','Cookie','Upgrade-Insecure-Requests','Sec-Fetch-Dest','Sec-Fetch-Mode','Sec-Fetch-Site','Sec-Fetch-User','Device-Memory','Dpr','Viewport-Width','Cache-Control']:
                if MySecurity.is_string_empty(header[x]) == False:
                    score += 2
                if x == "Cookie":
                    if "csrftoken" not in header[x] or "sessionid" not in header[x]:
                        score -= 50
                elif x == "User-Agent":
                    if str(header[x]).lower() != str(user_agent).lower():
                        score -= 30
                elif x == "Content-Type":
                    if "application/x-www-form-urlencoded" not in header[x]:
                        score -= 5
                elif x == "Accept-Encoding":
                    if "gzip" not in header[x]:
                        score -= 5
                elif x == "Connection":
                    if header[x] != "keep-alive":
                        score -= 5
                elif x == "Host":
                    if header[x] not in ["spunkydev.com", 'https://spunkydev.com', '127.0.0.1:8000', 'http://127.0.0.1:8000']:
                        score -= 5
        if score < 0:
            score = 0
        if score > 100:
            score = 100
        return {"score":100,"user_ip":user_ip,"user_width":user_width, "user_height":user_height,"user_colordepth":user_colordepth,"user_pixeldepth":user_pixeldepth,"user_historylength":user_historylength,"user_cookieok":user_cookieok,"user_language":user_language,"user_agent":user_agent,"user_navok":user_navok,"user_pdfok":user_pdfok,"user_hardware":user_hardware,"user_webdriverok":user_webdriverok,"user_adblocker":user_adblocker,"user_joining":user_joining,"user_darkmode":user_darkmode,"user_browser":user_browser,"user_os":user_os,"user_device":user_device,"user_country":user_country,"user_city":user_city,"user_referer":user_referer,}
    @staticmethod
    def verif_session_exist(request):
        if request.session.session_key is None:
            request.session['CURRENT_HEADER'] = request.headers['User-Agent']
            request.session['CURRENT_IP'] = MySecurity.get_ip(request)
            request.session['SCORE'] = 100
            first_visit = True
        else :
            first_visit = False
        return first_visit
    @staticmethod
    def verif_session_flight(request):
        last_request_header = request.session.get('CURRENT_HEADER', None)
        last_request_ip = request.session.get('CURRENT_IP', None)
        if last_request_header is None or last_request_header != request.headers['User-Agent']:
            request.session['CURRENT_HEADER'] = request.headers['User-Agent']
            score = request.session.get('SCORE', 0)
            value = 15
            if (score - value) < 0:
                score = 0
            else:
                score -= value
            request.session['SCORE'] = score
            MySecurity.update_user_score(request, score)
        if last_request_ip is None or last_request_ip != MySecurity.get_ip(request):
            if MyIpManagement.objects.filter(ip=MySecurity.get_ip(request)).values().count() == 0:
                request.session['SCORE'] = 50
                try:
                    MyIpManagement(
                        ip = MySecurity.get_ip(request),
                        score = 50,
                        start_date = str(timezone.now()),
                        last_request_date = str(timezone.now()),
                        total_request_count = 2,
                    ).save()
                except:
                    MyLog.internal_error_log(request.session.session_key, "Internal Error 1.53 >  MyIpManagement Insert Error in session_creation.")
                return True
            else:
                request.session['SCORE'] = 50
                MySecurity.update_user_score(request, 50)
        return True
    @staticmethod
    def verif_session_shadowban(request):
        if request.session.get('SHADOW', False):
            return True
        return False
    @staticmethod
    def is_pdf(file_path):
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            if pdf_reader.getNumPages() > 0:
                return True
            else:
                return False
    @staticmethod
    def verif_score(request, current_path : str):
        request.session['BEFORE_PATH'] = current_path 
        return False
        # if request.session.get('SCORE', 0) <= settings.MINIMUM_SCORE:
        #     MyLog.write_log(request.session.session_key, 'BOT_VERIFICATION_ASKED')
        #     request.session['SHADOW'] = True
        #     request.session['BEFORE_PATH'] = current_path 
        #     return True
        # return False
    @staticmethod
    def check_match(string_to_match = 'https://spunkydev.com/admin-login/', match_string = ['spunkydev.com']):
        for string in match_string:
            matcher = difflib.SequenceMatcher(a=string_to_match, b=string)
            match = matcher.find_longest_match(0, len(matcher.a), 0, len(matcher.b))
            if matcher.a[match.a:match.a+match.size] == string:
                return True
        return False
    @staticmethod
    def get_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return escape(ip)
    @staticmethod
    def post_antispam(request, title):
        return render(
            request, 
            'listings/firewall.html',
            {
                'default_title' : f'LinkGarden > {escape(title)}',
            }
        )
    @staticmethod
    def get_ban(request, title):
        if request.session.get('FULLBAN', False):
            try:
                data = MyIpBanList.objects.filter(ip = MySecurity.get_ip(request)).values("reason", "expiration_date").all()[:1][0]
            except:
                MyLog.internal_error_log(request.session.session_key, "Internal Error 1.54 > MyIpBanList can't get data.")
            return render(
                request, 
                'listings/ban.html',
                {
                    'default_title' : f'LinkGarden > {escape(title)}',
                    'expiration_date': escape(data['expiration_date'])[:19],
                    'reason': escape(data['reason']),
                    'description': 'Your suspicious activity make you temporarily ban from LinkGarden website. Ask for Spunky Development contact if you think that it is a mistake.',
                }
            )
    @staticmethod
    def kick_admin(request, kick_reason : str):
        MyLog.write_log(request.session.session_key, 'KICKED_FROM_ADMIN')
        MyLog.notif(f"An administrator has been kicked. REASON: {kick_reason} | IP: {MySecurity.get_ip(request)} | User-Agent: {request.headers['User-Agent']}")
        return redirect("logout")
    @staticmethod
    def verif_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else: 
            return False
    @staticmethod
    def verif_phone(phone):
        regex = r'\b^[0-9-=() ]{8,18}$\b'
        if re.fullmatch(regex, phone):
            return True
        else: 
            return False
    @staticmethod
    def verif_discord(discord):
        regex = r'\b^.{3,32}#[0-9]{4}$\b'
        if re.fullmatch(regex, discord):
            return True
        else: 
            return False
    @staticmethod
    def verif_name(name):
        regex = r'\b^[a-zA-Z-äÄâÂëËêÊïÏîÎöÖôÔüÜûÛ ]*$\b'
        if re.fullmatch(regex, name):
            return True
        else: 
            return False
    @staticmethod
    def verif_input(request, form_data : dict):
        if len(request) != len(form_data['input']):
            return False
        for x in form_data['input']:
            try:
                if MySecurity.is_string_empty(request[x]):
                    return False
            except:
                return False
        return True
    @staticmethod
    def verif_2FA_code(request, form_data : dict):
        if MySecurity.verif_input(request, form_data) != True:
            return False
        code = request['c1'] + request['c2'] + request['c3'] + request['c4'] + request['c5'] + request['c6'] + request['c7'] + request['c8'] + request['c9']
        return code
    @staticmethod
    def verif_spam_action(request, m_action, repeat_authorised = 5, interval = 120):
        try:
            result = MySessionLog.objects.filter(
                key = request.session.session_key, 
                action = escape(m_action), 
                date__range = [timezone.now() - timezone.timedelta(seconds=interval), timezone.now()]
            ).all().count()
        except:
            MyLog.internal_error_log(request.session.session_key, "Internal Error 1.55 > Error in verif_spam_action.")
        if result >= repeat_authorised:
            return True
        return False
    @staticmethod
    def clear_all_unexpected_space(s):
        data = str(s)
        unexpected = [" "," "," "," "," "," "," "," "," "," "," "," "," "," ","　"]
        for x in unexpected:
            data = str(data.replace(x,""))
        return data
    @staticmethod
    def is_string_empty(s):
        try:
            if isinstance(s, str) != True:
                return None
            vs = MySecurity.clear_all_unexpected_space(s)
        except:
            return True
        if vs is None or len(vs) == 0 or vs == "":
            return True
        return False
    @staticmethod
    def tri_decroissant(liste):
        n = len(liste)
        for i in range(n):
            max_idx = i
            for j in range(i+1, n):
                if liste[j]['note'] > liste[max_idx]['note']:
                    max_idx = j
            liste[i], liste[max_idx] = liste[max_idx], liste[i]
        return liste