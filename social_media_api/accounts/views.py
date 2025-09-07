from django.shortcuts import render
from rest_framework.serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from .models import CustomUser



# View for user registration
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Token login view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

["generics.GenericAPIView", "permissions.IsAuthenticated", "CustomUser.objects.all()"]

# Create your views here.

class Follow_User(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow = CustomUser.objects.get(pk=kwargs['pk'])
        request.user.following.add(user_to_follow)
        user_to_follow.followers.add(request.user)
        return Response({"message": "You are now following {}".format(user_to_follow.username)}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(pk=kwargs['pk'])
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
        return Response({"message": "You have unfollowed {}".format(user_to_unfollow.username)}, status=status.HTTP_200_OK)

class Unfollow_User(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(pk=kwargs['pk'])
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
        return Response({"message": "You have unfollowed {}".format(user_to_unfollow.username)}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
