import os
from django.conf import settings




def user_directory_path_profile(instance, filename):
    profile_picture_name = 'account/{0}/profile/profile.jpg'.format(instance.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path): os.remove(full_path)
    return profile_picture_name

def banner_directory_path_profile(instance, filename):
    profile_picture_name = 'account/{0}/profile/banner.jpg'.format(instance.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path): os.remove(full_path)
    return profile_picture_name


