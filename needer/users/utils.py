import os
from django.conf import settings
import random

def user_directory_path_profile(instance, filename):
    profile_picture_name = 'account/{0}/profile/profile{1}.jpg'.format(instance.username, random.randint(0,100))
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, 'account/{0}/profile/'.format(instance.username))
        lista_ficheros = os.listdir(full_path)
        if lista_ficheros[0].endswith(".jpg"):
            os.remove(full_path + lista_ficheros[0])
    except:
        return profile_picture_name
    return profile_picture_name

def banner_directory_path_profile(instance, filename):
    profile_picture_name = 'account/{0}/profile/banner{1}.png'.format(instance.username, random.randint(0,100))
    try:
        full_path = os.path.join(settings.MEDIA_ROOT, 'account/{0}/profile/'.format(instance.username))
        lista_ficheros = os.listdir(full_path)
        if lista_ficheros[0].endswith(".png"):
            os.remove(full_path + lista_ficheros[0])
    except:
        return profile_picture_name
    return profile_picture_name


