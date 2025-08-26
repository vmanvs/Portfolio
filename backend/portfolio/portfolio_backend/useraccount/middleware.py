class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (hasattr(request, '_jwt_data') and
            request.path.startswith('/accounts/') and
            response.status_code in [302 ,200]):
                print('This is working at least')

                access_token = request._jwt_data['access_token']
                refresh_token = request._jwt_data['refresh_token']

                response.set_cookie('access_token', access_token)
                response.set_cookie('refresh_token', refresh_token)

        print(response.cookies) #comment later

        return response