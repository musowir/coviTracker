from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from . models import CustomerProfile, UserPositivityLog

from usermanagement.serializers import (CustomerProfileSerializer, 
                            UserLoginSerializer, TokenSerializer, 
                            CustomerProfileUpdateSerializer, 
                            UserFeedbackSerializer)


class UserRegistration(generics.CreateAPIView):
    """ User Registration 
        params :
    """
    serializer_class = CustomerProfileSerializer
    def post(self, *args, **kwargs):
        # print(self.request.data)
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(
                    data={'token':None,
                        'user_data': None,
                        'masg':serializer.errors},
                        status=status.HTTP_200_OK,
                    )
        else:
            cust_obj = serializer.save()
            user_obj = cust_obj.user
            token, _ = Token.objects.get_or_create(user=user_obj)
            return Response(
                    data={'token':token.key,
                        'user_data': self.serializer_class(instance=cust_obj).data},
                        status=status.HTTP_200_OK,
                    )


class UserLoginAPIView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        print("Here is the call ", request.data)
        if not self.request.data.get('fcm_token'):
            return Response(
                data={'token':None,
                    'user_data': None,
                    'msg': "invalid FCM Token"},
                    status=status.HTTP_200_OK,
                )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.user_profile.fecm_token = self.request.data.get('fcm_token')
            token, _ = Token.objects.get_or_create(user=user)
            print(token)
            return Response(
                    data={'token':token.key,
                    'user_data': CustomerProfileSerializer(user.user_profile).data},
                    status=status.HTTP_200_OK,
                    )
        else:
            return Response(
                data={'token':None,
                    'user_data': None},
                    status=status.HTTP_200_OK,
                )


class UserExists(APIView):

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        username = request.data.get('username')
        phone_ = False
        email_ = False
        if User.objects.filter(username=username).exists():
            phone_ = True
        elif User.objects.filter(email=username).exists() and User.objects.filter(email=username).count() == 1:
            email_ = True

        if phone_ or email_:
            return Response(
                data={'is_existing' : True},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                data={'is_existing' : False},
                    status=status.HTTP_200_OK,
                )


class UpdateUserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileUpdateSerializer
    queryset = CustomerProfile.objects.all()

    def put(self, request, *args, **kwargs):
        # print("INSIDE PUT")
        # if not request.data.get('password'):
        data = super(UpdateUserProfile, self).put(request, *args, **kwargs)
        print("put", data, self.get_object())
        user_data ={
            "id": self.get_object().id,
            "phone_number": self.get_object().phone_number,
            "email": self.get_object().user.email,
            "gender": self.get_object().gender,
            "first_name": self.get_object().user.first_name,
            "last_name": self.get_object().user.last_name,
            "otp_verified": self.get_object().otp_verified,
            "covid_status": self.get_object().get_covid_status_display()
        }
        data = {
                "token": "9031f3a2b872b7fe2b5dac8ceb187977bd372e49",
                "user_data": {
                    "id": 32,
                    "phone_number": "9544073550",
                    "email": "aniridhdjdj@gmail.com",
                    "gender": "",
                    "first_name": "anirudh",
                    "last_name": "qwert",
                    "otp_verified": False,
                    "profile_pic1": "/media/profile_pic/image_dmf1Rf7.jpeg",
                    "profile_pic2": "/media/profile_pic/image_H9Ic6VD.jpeg",
                    "profile_pic3": "/media/profile_pic/image_mwdl1uc.jpeg",
                    "token": "9031f3a2b872b7fe2b5dac8ceb187977bd372e49",
                    "fcm_token": "fVbkpG0OT6yTvhBPXpd-_X:APA91bE8d1ESN1XpTc47ZH5njaezHLN_qE6wFBiuRDgLf3QPlRLS6HXYV3GkP_6neNmc2dBnmZuYuajrrvQNC6vp-WDLK82QJ7LSULPp12Bqy2khE6f7cPS6LB_aLi-6kAHTOZ_2emsQ",
                    "covid_status": "Negative"
                }
            }
            
        return Response(
                    data={'token':None, 'user_data': CustomerProfileSerializer(self.get_object()).data},
                    status=status.HTTP_200_OK,
                    )


class CreateFeedack(generics.CreateAPIView):
    serializer_class = UserFeedbackSerializer


class ChangeCovidStatus(APIView):
    model = CustomerProfile

    def post(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        try:
            user_ob = self.model.objects.get(id=id)
            if user_ob.covid_status == 'N':
                user_ob.covid_status = 'P'
            else:
                user_ob.covid_status = 'N'
            UserPositivityLog.objects.create(customer=user_ob, covid_status=user_ob.covid_status)
            user_ob.save()
            msg = "Successfully updated the covid status of " + user_ob.get_full_name().title()
            return Response({"msg": msg},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"msg": msg},status=status.HTTP_200_OK)