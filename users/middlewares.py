import jwt
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from jwt.exceptions import InvalidTokenError

from users.models import User
from django.middleware.csrf import get_token



class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = get_token(request)
        # Check if token is present in the header
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            try:
                # Extract the token from the header
                token = auth_header.split(' ')[1]

                # Verify and decode the token using the secret key
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.filter(id=decoded['id']).first()
                # Set the user as authenticated
                request.user = SimpleLazyObject(lambda:user)
            except InvalidTokenError:
                pass

        response = self.get_response(request)

        return response
