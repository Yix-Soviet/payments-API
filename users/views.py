from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, GetUserSerializer
from .tokens import create_jwt_pair_for_user
from rest_framework import viewsets
from .models import User


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "The user was created correctly",
                "data": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            idUser = User.objects.get(email=email)
            response = {
                "message": "Successfully logged in",
                "id": idUser.id,
                "tokens": tokens,
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or incorrect password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


class GetUsers(viewsets.ReadOnlyModelViewSet):
    serializer_class = GetUserSerializer
    queryset = User.objects.all()
