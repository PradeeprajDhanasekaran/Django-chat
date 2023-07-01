from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from api.serializers import UserSerializer
from .models import User, Message
from pathlib import Path

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    # user.online = True
    # user.save()

    refresh = RefreshToken.for_user(user)

    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(id=token.payload.get('user_id'))
    user.online = False
    user.save()
    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_online_users(request):
    query = User.objects.filter(online='True')
    data = UserSerializer(query, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_chat(request):
    channel_layer = get_channel_layer()
    # access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    receiver_id = request.data.get('receiver_id')
    my_id = request.user.username
    groupName = '-'.join(sorted([my_id,receiver_id]))
    channel_name = f"chat_{groupName}" 

    async def add_user_to_group(channel_name, user_id):
        await channel_layer.group_add(f"chat_{user_id}", channel_name)
    async_to_sync(add_user_to_group)(channel_name, my_id)
    async_to_sync(add_user_to_group)(channel_name, receiver_id)
    receiver = User.objects.filter(username=receiver_id)
    if receiver.exists():
        if receiver.first().online:
            return Response({'message': 'User is available to receive messages'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User is unavailable'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response('connected', status=status.HTTP_200_OK)
def get_user_id_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return user_id
    except Exception as e:
        raise AuthenticationFailed('Invalid access token')



@api_view(['GET'])
def suggested_friends(request, user_id):
    BASE_DIR = Path(__file__).resolve().parent.parent
   
    with open(BASE_DIR/'users.json') as f:
        data = json.load(f)
    

    user = None
    for item in data['users']:
        if item['id'] == user_id:
            user = item
            break

    if user is None:
        print(f"User {user_id} not found.")
        exit()

    def calculate_similarity(user1, user2):
        interests1 = user1['interests']
        interests2 = user2['interests']
        common_interests = set(interests1.keys()).intersection(set(interests2.keys()))

        num_common_interests = len(common_interests)

        score = 0
        for interest in common_interests:
            score += abs(interests1[interest] - interests2[interest])

        return num_common_interests, score

    similarity_scores = []
    for item in data['users']:
        if item['id'] != user_id:
            similarity = calculate_similarity(user, item)
            similarity_scores.append((item['id'], similarity))

    similarity_scores.sort(key=lambda x: (x[1][0], -x[1][1]), reverse=True)

    suggested_friends = similarity_scores[:5]

    suggested_friends_details = []
    for friend_id, _ in suggested_friends:
        for item in data['users']:
            if item['id'] == friend_id:
                suggested_friends_details.append(item)
                break
    return Response(suggested_friends_details, status=status.HTTP_200_OK)