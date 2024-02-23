from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from keycloak import KeycloakOpenID
from django.conf import settings
from django.urls import reverse
from dater.views import login_view
from django.shortcuts import redirect
from urllib.parse import urlencode
import jwt
from showdate.validitycheck import check_token


def index(request):
    client = KeycloakOpenID(server_url=settings.KEYCLOAK_AUTHORIZATION_URL,
                            realm_name=settings.KEYCLOAK_REALM,
                            client_id=settings.KEYCLOAK_CLIENT_ID)

    if 'access_token' in request.session:
        token = request.session['access_token']
        #token = client.decode_token(token=request.session['access_token'])
        check_token(token)
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        if decoded_token:
            username = decoded_token['preferred_username']
            return render(request, 'index.html', {'username': username})

    return HttpResponseRedirect(reverse('login'))


def showdate(request):
    return HttpResponse("Todays Date: 21st Feb 2024")
