from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter): #save method is called during callback URL processing not before
    def save_user(self, request, sociallogin, form=None):

            user = super().save_user(request, sociallogin, form)

            refresh = RefreshToken.for_user(sociallogin.user)
            access = refresh.access_token

            request._jwt_data = {
                "access_token": str(access),
                "refresh_token": str(refresh),
                "user" : {
                "id": user.id,
                "email": user.email,
                },
            }

            #print(request.session['_jwt_data'])

            return user

    def pre_social_login(self, request, sociallogin):

        if sociallogin.user:
            refresh = RefreshToken.for_user(sociallogin.user)
            access = refresh.access_token

            request._jwt_data = {
                "access_token": str(access),
                "refresh_token": str(refresh),
                "user" : {
                    "id": sociallogin.user.id,
                    "email": sociallogin.user.email,

                }
            }

