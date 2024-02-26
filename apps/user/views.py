""" core/views.py """
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login

from .models import CustomUser, Profile
from .serializers import (
    UserSerializer, LoginSerializer,
    ForgotPasswordSerializer, ChangePasswordSerializer,
    ProfileEditSerializer
)


class UserCreateAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "message": "success",
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
                {

                    "message": "failed",
                    'data': serializer.errors,
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data

                if user is not None:
                    login(request, user)

                refresh = RefreshToken.for_user(user)
                serialized_user = UserSerializer(user).data

                return Response({
                    'status': status.HTTP_200_OK,
                    'message': "User Successfully Login",
                    'user': serialized_user,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                },
                    status=status.HTTP_200_OK
                )
        except Exception as err:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'errors': str(err),
                'message': "User login unsuccessfull."
                }
            )


class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "message": "success",
                    'data': serializer.data,
                    'status': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {

                    "message": "failed",
                    'data': serializer.errors,
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordAPIView(APIView):

    # def get_object(self):
    #     breakpoint()
    #     return True

    def update(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        breakpoint()
        if serializer.is_valid():
            print(uuid)
            user_uuid = kwargs.get('uuid')
            password = serializer.data.get('password')
            user = self.get_object()
            # user = CustomUser.objects.get(uuid=user_uuid)
            user.set_password(password)
            user.save()

            return Response(
                {
                    "message": "success",
                    'data': serializer.data,
                    'status': status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        return Response(
                {

                    "message": "failed",
                    'data': serializer.errors,
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileEditAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = ProfileEditSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                response = {
                    'data': serializer.data,
                    'message': "Successfully updated profile",
                    'status': status.HTTP_200_OK
                }
                return Response(
                    response,
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'errors': serializer.errors,
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            )
        except Exception as e:
            return Response(
                {
                    'errors': e,
                    'message': "Profile not updated",
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
