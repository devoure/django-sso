import requests
from django.conf import settings


def check_token(token):
    server_url = settings.KEYCLOAK_INSPECT_URL
    realm_name = settings.KEYCLOAK_REALM
    introspection_endpoint = settings.KEYCLOAK_INSPECT_URL

    client_id = settings.KEYCLOAK_CLIENT_ID
    client_secret = settings.KEYCLOAK_CLIENT_SECRET

    payload = {
            'token': token,
            'client_id': client_id,
            'client_secret': client_secret,
            'realm_name':realm_name
            }
    res = requests.post(introspection_endpoint, data=payload)

    if res.status_code == 200:
        is_valid = res.json()['active']
        print(">>>", is_valid)
        if is_valid:
            print("valid")
        else:
            print("not valid")
