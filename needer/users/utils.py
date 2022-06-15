import json
import os
from django.conf import settings
from marketplace.models import Access_Token_Paypal
import requests
import hashlib




def user_directory_path_profile(instance, filename):
    profile_picture_name = 'account/{0}/profile/profile.jpg'.format(instance.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path): os.remove(full_path)
    return profile_picture_name

def get_access_token():
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    data = {"grant_type": "client_credentials",
            'Content-Type': 'application/json'}
    auth =(settings.PAYPAL_CLIENT_ID, 
    settings.PAYPAL_SECRET_ID)
    response = requests.post(url,data, auth=auth)
    
    if response.status_code not in [200]:
      return 'ERROR TOKEN'

    token = Access_Token_Paypal.objects.get(pk=1) 
    token.access_token =  'Bearer ' + response.json()['access_token']
    token.save()
    return token.access_token




def get_action_url(token):
    tracking_id =hashlib.sha256().hexdigest()
    url = 'https://api-m.sandbox.paypal.com/v2/customer/partner-referrals'
    data={
      "preferred_language_code": "es-CO",
      "tracking_id": tracking_id,
      "partner_config_override": {
        "partner_logo_url": "https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg",
        "return_url": "http://127.0.0.1:8000/accounts/profile/",
        "return_url_description": "the url to return the merchant after the paypal onboarding process.",
        "action_renewal_url": "http://needer.com.co",
        "show_add_credit_card": True
      },
      "operations": [
        {
          "operation": "API_INTEGRATION",
          "api_integration_preference": {
            "rest_api_integration": {
              "integration_method": "PAYPAL",
              "integration_type": "THIRD_PARTY",
              "third_party_details": {
                "features": [
                  "PAYMENT",
                  "REFUND"
                ],
              }
            }
          }
        }
      ],
      
      "legal_consents": [
        {
          "type": "SHARE_DATA_CONSENT",
          "granted": True
        }
      ],
      "products": [
        "EXPRESS_CHECKOUT"
      ]
    }
    response = requests.post(url=url,headers={'Content-Type': 'application/json',
    'Authorization':token}, data=json.dumps(data))
    
    if response.status_code not in [201]:
        
        token = get_access_token()
        response = requests.post(url=url,headers={'Content-Type': 'application/json',
        'Authorization':token}, data=json.dumps(data))

    return response.json()['links'][1]['href']