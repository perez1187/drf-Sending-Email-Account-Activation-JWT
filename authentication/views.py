import email
import imp
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . serializers import RegisterSerializer

# for jwt and sending email
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer

    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data= serializer.data

        # after create user we create token
        user=User.objects.get(email=user_data['email'])
        token =RefreshToken.for_user(user).access_token

        # sending email
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify') # urls and name=


        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi ' + ' use link bellow to verify your email \n' + absurl
        data = {
            'email_body': email_body,
            'email_subject': 'Verify your email',
            'to_email': 'o.perez1187@gmail.com'

        }
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass