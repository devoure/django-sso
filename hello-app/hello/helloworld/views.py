from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from keycloak import KeycloakOpenID
from django.conf import settings
from django.urls import reverse
from hello.views import login_view
from django.shortcuts import redirect
from urllib.parse import urlencode
from helloworld.validitycheck import check_token
import jwt

# Create your views here.
def helloworld(request):
    if 'access_token' in request.session:
        token = request.session['access_token']
        #token = client.decode_token(token=request.session['access_token'])
        check_token(token)
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        if decoded_token:
            username = decoded_token['preferred_username']
            return render(request, 'index.html', {'username': username})

    return HttpResponseRedirect(reverse('login'))
