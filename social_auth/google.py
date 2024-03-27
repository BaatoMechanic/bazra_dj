from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    @staticmethod
    def validate(auth_token):
        try:

            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)

            # if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            #     raise ValueError('Wrong issuer.')
            if 'accounts.google.com' in idinfo['iss']:
                # print('he')
                # print(idinfo)
                return idinfo

        # except:
        #     return "Token either expired or invalid"
        except Exception as e:
            print(e)
            return "Token either expired or invalid"
