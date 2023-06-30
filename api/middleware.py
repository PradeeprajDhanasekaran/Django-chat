import json
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status


@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user = token.payload.get('user_id')
        return User.objects.get(id=user)
    except (TokenError, User.DoesNotExist):
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        token_key = headers.get(b"authorization", b"")
        user = await get_user(token_key)
        
        if user.is_anonymous:
            error_message = {'error': 'Login to send message'}
            await send({
            'type': 'websocket.close',
            'code': 1008,
            'text': json.dumps(error_message),
        })
        
        scope['user'] = user
        
        return await super().__call__(scope, receive, send)
