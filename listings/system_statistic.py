#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
import difflib
from django.utils import timezone
from listings.models import MyTraficData, MyStatisticData, MyVisitor
class MyStatisticAction:
    def increment_trafic(inc_data : str) -> bool:
        if inc_data not in ['get_trafic', 'post_trafic', 'total_trafic', 'session_trafic', 'ip_trafic', 'referal_trafic', 'direct_trafic', 'browser_trafic']:
            return False
        day = str(timezone.now())[:10]
        try:
            c_stat = MyTraficData.objects.filter(date = day).values().get()
        except:
            c_stat = {}
        if len(c_stat) == 0:
            MyTraficData(get_trafic = 0,post_trafic = 0,total_trafic = 0,session_trafic = 0,ip_trafic = 0,referal_trafic = 0,direct_trafic = 0,browser_trafic = 0,date = day).save()
            c_stat = {'get_trafic': 0,'post_trafic': 0, 'total_trafic': 0, 'session_trafic': 0,'ip_trafic': 0,'referal_trafic':0,'direct_trafic':0,'browser_trafic':0,}
        if inc_data == "get_trafic":
            MyTraficData.objects.filter(date = day).update(get_trafic = int(c_stat["get_trafic"]) + 1, total_trafic = int(c_stat["total_trafic"]) + 1)
            MyStatisticAction.increment_stats('total_get_trafic')
        elif inc_data == "post_trafic":
            MyTraficData.objects.filter(date = day).update(post_trafic = int(c_stat["post_trafic"]) + 1, total_trafic = int(c_stat["total_trafic"]) + 1)
            MyStatisticAction.increment_stats('total_post_trafic')
        elif inc_data == "total_trafic":
            MyTraficData.objects.filter(date = day).update(total_trafic = int(c_stat["total_trafic"]) + 1)
        elif inc_data == "session_trafic":
            MyTraficData.objects.filter(date = day).update(session_trafic = int(c_stat["session_trafic"]) + 1)
            MyStatisticAction.increment_stats('total_session_trafic')
        elif inc_data == "ip_trafic":
            MyTraficData.objects.filter(date = day).update(ip_trafic = int(c_stat["ip_trafic"]) + 1)
        elif inc_data == "referal_trafic":
            MyTraficData.objects.filter(date = day).update(referal_trafic = int(c_stat["referal_trafic"]) + 1)
        elif inc_data == "direct_trafic":
            MyTraficData.objects.filter(date = day).update(direct_trafic = int(c_stat["direct_trafic"]) + 1)
        elif inc_data == "browser_trafic":
            MyTraficData.objects.filter(date = day).update(browser_trafic = int(c_stat["browser_trafic"]) + 1)
        return True
    def get_main_stats() -> dict or bool:
        try:
            statistic = MyStatisticData.objects.filter(id = 1).values()[:1].get()
        except:
            return False
        return statistic
    def increment_stats(inc_data) -> bool:
        if inc_data not in ['windows','mac','linux','android','ios','other_os','chrome','firefox','edge','safari','opera','other_browser','desktop','tablet','mobile','from_referal','from_direct','from_browser','total_get_trafic','total_post_trafic','total_session_trafic','total_ip_trafic']:
            return False
        statistic = MyStatisticAction.get_main_stats()
        if statistic == False:
            return False
        if inc_data == "windows":
            MyStatisticData.objects.filter(id = 1).update(windows = int(statistic["windows"]) + 1)
        elif inc_data == "mac":
            MyStatisticData.objects.filter(id = 1).update(mac = int(statistic["mac"]) + 1)
        elif inc_data == "linux":
            MyStatisticData.objects.filter(id = 1).update(linux = int(statistic["linux"]) + 1)
        elif inc_data == "android":
            MyStatisticData.objects.filter(id = 1).update(android = int(statistic["android"]) + 1)
        elif inc_data == "ios":
            MyStatisticData.objects.filter(id = 1).update(ios = int(statistic["ios"]) + 1)
        elif inc_data == "other_os":
            MyStatisticData.objects.filter(id = 1).update(other_os = int(statistic["other_os"]) + 1)
        elif inc_data == "chrome":
            MyStatisticData.objects.filter(id = 1).update(chrome = int(statistic["chrome"]) + 1)
        elif inc_data == "firefox":
            MyStatisticData.objects.filter(id = 1).update(firefox = int(statistic["firefox"]) + 1)
        elif inc_data == "edge":
            MyStatisticData.objects.filter(id = 1).update(edge = int(statistic["edge"]) + 1)
        elif inc_data == "safari":
            MyStatisticData.objects.filter(id = 1).update(safari = int(statistic["safari"]) + 1)
        elif inc_data == "opera":
            MyStatisticData.objects.filter(id = 1).update(opera = int(statistic["opera"]) + 1)
        elif inc_data == "other_browser":
            MyStatisticData.objects.filter(id = 1).update(other_browser = int(statistic["other_browser"]) + 1)
        elif inc_data == "desktop":
            MyStatisticData.objects.filter(id = 1).update(desktop = int(statistic["desktop"]) + 1)
        elif inc_data == "tablet":
            MyStatisticData.objects.filter(id = 1).update(tablet = int(statistic["tablet"]) + 1)
        elif inc_data == "mobile":
            MyStatisticData.objects.filter(id = 1).update(mobile = int(statistic["mobile"]) + 1)
        elif inc_data == "from_referal":
            MyStatisticData.objects.filter(id = 1).update(from_referal = int(statistic["from_referal"]) + 1)
        elif inc_data == "from_direct":
            MyStatisticData.objects.filter(id = 1).update(from_direct = int(statistic["from_direct"]) + 1)
        elif inc_data == "from_browser":
            MyStatisticData.objects.filter(id = 1).update(from_browser = int(statistic["from_browser"]) + 1)
        elif inc_data == "total_get_trafic":
            MyStatisticData.objects.filter(id = 1).update(total_get_trafic = int(statistic["total_get_trafic"]) + 1)
        elif inc_data == "total_post_trafic":
            MyStatisticData.objects.filter(id = 1).update(total_post_trafic = int(statistic["total_post_trafic"]) + 1)
        elif inc_data == "total_session_trafic":
            MyStatisticData.objects.filter(id = 1).update(total_session_trafic = int(statistic["total_session_trafic"]) + 1)
        elif inc_data == "total_ip_trafic":
            MyStatisticData.objects.filter(id = 1).update(total_ip_trafic = int(statistic["total_ip_trafic"]) + 1)
        return True
    @staticmethod
    def reset_statistic():
        MyStatisticData.objects.filter(id = 1).update(windows = 0,mac = 0,linux = 0,android = 0,ios = 0,other_os = 0,chrome = 0,firefox = 0,edge = 0,safari = 0,opera = 0,other_browser = 0,desktop = 0,tablet = 0,mobile = 0,from_referal = 0,from_direct = 0,from_browser = 0,total_get_trafic = 0,total_ip_trafic = 0,total_post_trafic = 0,total_session_trafic = 0,)
        return True
    @staticmethod
    def update_statistic(request, data):
        user_os = data["user_os"]
        user_browser = data["user_browser"]
        user_device = data["user_device"]
        user_referer = data["user_referer"]
        user_ip = data["user_ip"]
        if user_os == 'Windows':
            MyStatisticAction.increment_stats('windows')
        elif user_os == 'MacOS':
            MyStatisticAction.increment_stats('mac')
        elif user_os == 'Linux':
            MyStatisticAction.increment_stats('linux')
        elif user_os == 'Android':
            MyStatisticAction.increment_stats('android')
        elif user_os == 'iOS':
            MyStatisticAction.increment_stats('ios') 
        else:
            MyStatisticAction.increment_stats('other_os')
        if user_browser == 'Chrome'  or user_browser == "Mobile Chrome":
            MyStatisticAction.increment_stats('chrome')
        elif user_browser == 'Firefox':
            MyStatisticAction.increment_stats('firefox')
        elif user_browser == 'Edge':
            MyStatisticAction.increment_stats('edge')
        elif user_browser == 'Safari' or user_browser == "Mobile Safari":
            MyStatisticAction.increment_stats('safari')
        elif user_browser == 'Opera':
            MyStatisticAction.increment_stats('opera')
        else:
            MyStatisticAction.increment_stats('other_browser')
        if user_device == 'Tablet':
            MyStatisticAction.increment_stats('tablet')
        elif user_device == 'Mobile':
            MyStatisticAction.increment_stats('mobile')
        elif user_device == 'Desktop':
            MyStatisticAction.increment_stats('desktop')
        navigator = ["google.com","duckduckgo.com","bing.com","msn.com","qwant.com","brave.com","ecosia.org","you.com","yahoo.com","baidu.com","yandex.com","neeva.com","startpage.com","swisscows.com","onesearch.com","searchencrypt.com",]
        website = ["spunkydev.com","spunkydev.org",]
        social_media = ["discord.com","telegram.org","instagram.com","youtube.com","facebook.com","twitter.com","tiktok.com","spotify.com","whatsapp.com","wikipedia.com","linkedin.com",]
        if MyStatisticAction.check_match(str(user_referer), navigator):
            MyStatisticAction.increment_stats('from_browser')
            MyStatisticAction.increment_trafic('browser_trafic')
        elif MyStatisticAction.check_match(str(user_referer), website):
            MyStatisticAction.increment_stats('from_direct')
            MyStatisticAction.increment_trafic('direct_trafic')
        elif MyStatisticAction.check_match(str(user_referer), social_media):
            MyStatisticAction.increment_stats('from_referal')
            MyStatisticAction.increment_trafic('referal_trafic')
        if MyVisitor.objects.filter(ip = user_ip, date__range = [str(timezone.now())[:10], str(timezone.now() + timezone.timedelta(days=1))[:10]]).values().count() == 0:
            MyStatisticAction.increment_trafic('ip_trafic')
        try:
            if MyVisitor.objects.filter(ip = user_ip).values().count() == 0:
                MyStatisticAction.increment_stats('total_ip_trafic')
            if MyVisitor.objects.filter(ip = user_ip, date__range = [str(timezone.now())[:10], str(timezone.now() + timezone.timedelta(days=1))[:10]]).values().count() == 0:
                MyStatisticAction.increment_trafic('ip_trafic')
        except:
            return False
        return True
    def check_match(string_to_match = 'https://link-garden.com/', match_string = ['link-garden.com']):
        for string in match_string:
            matcher = difflib.SequenceMatcher(a=string_to_match, b=string)
            match = matcher.find_longest_match(0, len(matcher.a), 0, len(matcher.b))
            if matcher.a[match.a:match.a+match.size] == string:
                return True
        return False