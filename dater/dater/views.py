# views.py
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from keycloak import KeycloakOpenID
from django.conf import settings
from urllib.parse import urlencode

def login_view(request):
    # Initialize KeycloakOpenID instance
    keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_AUTHORIZATION_URL,
                                     client_id=settings.KEYCLOAK_CLIENT_ID,
                                     realm_name=settings.KEYCLOAK_REALM)
    redirect_uri = request.build_absolute_uri(reverse('index'))
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
    return redirect(reverse('index'))
