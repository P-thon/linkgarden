#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
import requests, re, tweepy
from bs4 import BeautifulSoup
from django.conf import settings
class MyExternalRequest:
    def telegram_send(text):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding": "gzip, deflate, sdch, br","Connection": "keep-alive"}
            result = requests.get(f"https://api.telegram.org/bot6266458858:AAEz8Kud_3Cso9lGtAWpGWDjImTAHXVL53E/sendMessage?chat_id=-944678939&text={str(text)}", headers=headers)
            if result.json()['ok'] != True:
                return False
        except:
            return False
        return True

    def send_notification(text):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding": "gzip, deflate, sdch, br","Connection": "keep-alive"}
            result = requests.get(f"https://api.telegram.org/bot5921689149:AAGVWC87aSMDIikQTtVaaArFNE6RPatyZIU/sendMessage?chat_id=-944678939&text={str(text)}", headers=headers)
            if result.json()['ok'] != True:
                return False
        except:
            return False
        return True
    @staticmethod
    def get_instagram_followers(username):
        try:
            result = requests.get(f"https://www.instagram.com/{username}/")
            if result.status_code != 200:
                return f"NULL #{result.status_code}"
            soup = BeautifulSoup(result.content, 'html.parser')
            followers = soup.find('meta', {'name': 'description'})['content']
            follower_count = followers.split('Followers')[0]
            return follower_count
        except:
            return "NULL #2"
    def extract_numbers(text : str) -> str or None:
        match = re.search(r'\b\d{1,3}(,\d{3})*\b', text)
        if len(match.group(0)) == 0 or match.group(0) is None:
            return None
        return match.group(0)