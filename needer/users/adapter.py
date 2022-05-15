from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        print('no existe')  
        user = sociallogin.user
        if user.id:  
            return print('no existe')     
        try:
            print('existe')   
            customer = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            perform_login(request, customer, 'none')
        except User.DoesNotExist:
            pass