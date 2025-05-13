#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : SDEV - spunkydev.com
from django.utils.translation import get_language_from_request
class MyLanguage:
    @staticmethod
    def change_current_language(request, language):
        request.session['language'] = "FR"
        # if language == 'French':
        #     request.session['language'] = 'FR'
        # elif language == 'English':
        #     request.session['language'] = 'EN'
    @staticmethod
    def verif_current_language(request, language):
        if language is None or language not in ['EN','FR']:
            language = MyLanguage.get_most_appropriate_language(request)
        if language not in ['EN','FR']:
            language = "FR" # Default
        return language
    @staticmethod
    def get_most_appropriate_language(request) -> str:
        # try:
        #     to_set_language = get_language_from_request(request).upper()
        # except:
        #     request.session['language'] = 'EN'
        # if to_set_language in ['FR', 'EN']:
        #     request.session['language'] = to_set_language
        # else:
        #     request.session['language'] = 'EN'
        # return request.session['language']
        request.session['language'] = 'FR'
    @staticmethod
    def get_view(request, template_page):
        try:
            return f"listings/public/{str(request.session['language'])}/{template_page}"
        except:
            return f"listings/public/{MyLanguage.get_most_appropriate_language(request)}/{template_page}"
    @staticmethod
    def get_status_with_good_language(cl, sta):
        if cl != "EN":
            
            if cl == "FR" and sta == "Please wait before trying again.":

                return "Veuillez patienter avant de réessayer."

            elif cl == "FR" and sta == "This email is already in our Newsletter.":

                return "Cette email est déjà dans notre newsletter."

            elif cl == "FR" and sta == "Invalid POST data.":

                return "Données POST invalides."

            elif cl == "FR" and sta == "Invalid email.":

                return "Email invalide."

            elif cl == "FR" and sta == "Email perfectly add to our newsletter.":

                return "Votre email a parfaitement été ajouté à notre Newsletter."

            elif cl == "FR" and sta == "BIRD":

                return "OISEAU"

            elif cl == "FR" and sta == "CAT":

                return "CHAT"

            elif cl == "FR" and sta == "FISH":

                return "POISSON"

            elif cl == "FR" and sta == "HORSE":

                return "CHEVAL"

            elif cl == "FR" and sta == "LION":

                return "LION"

            elif cl == "FR" and sta == "Internal error. We have been notified. This problem will be fixed as soon as possible.":

                return "Erreur interne. Nous avons été notifié. Ce problème sera fixé aussi vite que possible."

            elif cl == "FR" and sta == "You have been unbanned.":

                return "Vous avez été débannit."

            elif cl == "FR" and sta == "You have been banned, wait 5 min before trying again.":

                return "Vous avez été bannit, attendez 5 miniutes avant de réessayer."

            elif cl == "FR" and sta == "Please wait 10s before trying again.":

                return "Veuillez attendre 10 secondes avant de réessayer."

            elif cl == "FR" and sta == "Invalid username or password.":

                return "Nom d'utilisateur ou mot de passe incorrect."

            elif cl == "FR" and sta == "Message perfectly send.":

                return "Message parfaitement envoyé."
        return sta