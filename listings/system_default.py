
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
import base64, os, secrets, time
from colorama import Fore
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from datetime import datetime
from django.utils.html import escape
from listings.system_log import MySessionLog
class MyRandom:
    @staticmethod
    def get_random_string(lenght : int, strong : bool = False) -> str :
        result = ""
        string = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z", "A", "B", "C", "D", "E", "F", "G", "H" , "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        if(strong):
            string = string + ["~", "!" , "@" , "#" ,"$" ,"%" ,"^" ,"&" ,"*" ,"(" ,")" ,"-" ,"_" ,"=" ,"+" ,"[" ,"]" ,"{", "}", ",", ".", "<", ">", "/", "?"]
        for i in range (lenght):
            letter = secrets.choice(string)
            result = result + letter
        return result
    @staticmethod
    def generate_token():
        return MyRandom.get_random_string(32)
    @staticmethod
    def get_random_number_str(lenght : int) -> str:
        result = ""
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range (lenght):
            number = secrets.choice(number_list)
            result = result + number
        return result
class MyCrypto():
    def __init__(self):
        self.__kcache = {}
    def __derive_key(self, password, salt=None):
        ckey = (password, salt)
        if ckey in self.__kcache:
            return self.__kcache[ckey]
        if salt is None:
            salt = os.urandom(16)
        key = Scrypt(salt, 32, 2**16, 8, 1, default_backend()).derive(password)
        self.__kcache[ckey] = [salt, key]
        return salt, key
    def sym_encrypt(self, plaintext, password, b64=True, already_bytes=False):
        version = b''
        salt, key = self.__derive_key(password.encode('utf-8'))
        nonce = os.urandom(12)
        if already_bytes:
            ciphertext = ChaCha20Poly1305(key).encrypt(nonce, plaintext, None)
        else:
            ciphertext = ChaCha20Poly1305(key).encrypt(nonce, plaintext.encode('utf-8'), None)
        if b64:
            return base64.b64encode(version + salt + nonce + ciphertext).decode('utf-8')
        else:
            return version + salt + nonce + ciphertext
    def sym_decrypt(self, ciphertext : str, password):
        try:
            ciphertext = base64.b64decode(ciphertext)
        except:
            return None
        try:
            key = self.__derive_key(password.encode('utf-8'), ciphertext[1:17])[1]
            return ChaCha20Poly1305(key).decrypt(ciphertext[17:29], ciphertext[29:], None).decode('utf-8')
        except InvalidTag:
            return None
class MyTime:
    @staticmethod
    def time_checker(time_to_check : str, s_time : int):
        b = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
        try:
            a = datetime.strptime(str(time_to_check)[:-6], '%Y-%m-%d %H:%M:%S.%f')
            diff = b - a
        except:
            a = datetime.strptime(str(time_to_check), '%Y-%m-%d %H:%M:%S.%f')
            diff = b - a
        if s_time >= diff.seconds:
            return True
        return False
    @staticmethod
    def check_last_time_from_log(request, m_action, time : int = 10):
        try:
            result = MySessionLog.objects.filter(key = request.session.session_key, action = escape(m_action)).values().order_by('-date')[:1].get()
            date = result['date']
        except:
            return False
        if date is None:
            return False
        return MyTime.time_checker(date, time)
    @staticmethod
    def get_date_from_date(time):
        new_time = str(time)[:10].replace('-', '/')
        return new_time
    @staticmethod
    def get_time_from_date(time):
        new_time = str(time)[:19].replace('-', '/')[10:]
        return new_time