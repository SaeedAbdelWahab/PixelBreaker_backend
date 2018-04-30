from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .csrf_ignore import CsrfExemptSessionAuthentication,BasicAuthentication
from .serializers import *
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from Detection.ssocr import *
from Detection.ImageProject import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

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
            x = self.request.user.id  ## To send the user status in the state with the response ##
            p = User.objects.get(id=x)
            data = {"valid": True,"staff":p.is_staff, "errors": ""}
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

class test(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication) #use this line for every api tht uses self.request.user
    def post(self, request):
        user = self.request.user #get the user object which contains the email and id and other attributes of currently logged in user
        if not self.request.user.is_anonymous : 
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED )
        else : 
            return Response({"valid":False}, status=status.HTTP_400_BAD_REQUEST)        

class ImageDetailsView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request,format=None) :
        data = request.data      
        serializer_class = ImageDetailsSerializer(data=data)
        if serializer_class.is_valid():
            obj = serializer_class.save()   
            path = str(obj.image)
            id = obj.id
            print (path)
            preprocess(path)
            digits,img = detect_digits('test.bmp')
            cv2.imwrite(path+'_processes',img)
            reading = ''.join(str(x) for x in digits)
            im = ImageDetails.objects.get(id=id)
            im.reading=reading
            im.save()
            return Response({'path':path,'reading':reading}, status=status.HTTP_201_CREATED)
        return Response({'valid':False ,'errors':serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)


class  CustomerView(APIView) :
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request,number) :
        images = ImageDetails.objects.filter(number=number)
        if (images) :
            serializer = ImageDetailsSerializer(images,many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else : 
            return Response({'valid':False}, status=status.HTTP_400_BAD_REQUEST)    
