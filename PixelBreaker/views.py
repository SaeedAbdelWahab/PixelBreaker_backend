from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .csrf_ignore import CsrfExemptSessionAuthentication,BasicAuthentication

class Register(APIView):
    """ 
    Creates the user. 
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    """
    Login the user
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

		###### If the User is valid ######
        if user:
            login(request, user)
            serializer = UserSerializer(user)
            x = self.request.user  ## To send the user status in the state with the response ##
            data = {"valid": True, "errors": ""}
            return Response(data, status=status.HTTP_202_ACCEPTED )
        ###### If the User isn't valid ######
        if not user:
            txt = {'valid' : False , 'errors' : "Invalid Username or Password"}
            return Response(txt, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView) :
    """
    Logout the user
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        logout(request)
        return Response({"valid": True}, status=status.HTTP_200_OK)