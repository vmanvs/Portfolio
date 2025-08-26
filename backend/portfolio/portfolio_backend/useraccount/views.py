from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView

def home(request):
    return render(request, 'home.html')


def custom_tokens(request):
    print(request.session.get('_jwt_data'))
    jwt_data = request.session.get('_jwt_data')
    print(jwt_data)


    #refresh_token = RefreshToken.for_user(user)
    #access_token = refresh_token.access_token

    #data = {
    #    'user': {
    #        'id': user.id,
    #        'email': user.email,
    #    },
    #    'access-token': access_token,
    #    'refresh-token': refresh_token,
    #}

    if jwt_data:

        print('JWT data received')

        response = HttpResponseRedirect('/')
        response.set_cookie(
            'access_token',
            jwt_data['access_token'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax'
        )

        response.set_cookie(
            'refresh_token',
            jwt_data['refresh_token'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax'
        )

        request.session.flush()

        return response

    print('this is fucked')

    return JsonResponse('Invalid Login', status=404)




