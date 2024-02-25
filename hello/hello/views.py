# views.py
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import redirect
from keycloak import KeycloakOpenID
from django.conf import settings
from urllib.parse import urlencode
import requests

def login_view(request):
    # Initialize KeycloakOpenID instance
    keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_AUTHORIZATION_URL,
                                     client_id=settings.KEYCLOAK_CLIENT_ID,
                                     realm_name=settings.KEYCLOAK_REALM)
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    # Constructing the authorization URL
    authorization_url = 'http://127.0.0.1:8080/auth/realms/testrealm/protocol/openid-connect/auth?'
    authorization_url += urlencode({
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'response_type': 'code',
        'state': 'some_state',
        'redirect_uri': redirect_uri
    })
    # Redirect to Keycloak login page
    return redirect(authorization_url)

def logout_view(request):
    # Clear session data and redirect to logout URL
    request.session.clear()
    return redirect(reverse('logout'))


def callback_view(request):
    #client = KeycloakOpenID(server_url=settings.KEYCLOAK_TOKEN_URL,
     #                       realm_name=settings.KEYCLOAK_REALM,
     #                       client_id=settings.KEYCLOAK_CLIENT_ID)

    
    code = request.GET.get('code')
    #state = request.GET.get('state')

    #if not code or not state:
    #    return HttpResponseBadRequest('Invalid callback params')

    redirect_uri = request.build_absolute_uri(reverse('callback'))
    token_url = settings.KEYCLOAK_TOKEN_URL
    payload = {
            'grant_type': 'authorization_code',
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': redirect_uri
            }

    #token = client.token(grant_type='authorization_code',
    #                     code=code,
    #                     redirect_uri=redirect_uri)

    response = requests.post(token_url, data=payload)
    print("res >>.", response)

    if response.status_code == 200:
        token = response.json()
        access_token = token.get('access_token')
        request.session['access_token'] = access_token
    else:
        return HttpResponseBadRequest('Access token not found')

    #if 'access_token' in token:
    #    request.session['access_token'] = token['access_token']
    #else:
    #    return HttpResponseBadRequest('Access token not found in response')

    return redirect(reverse('helloworld'))
