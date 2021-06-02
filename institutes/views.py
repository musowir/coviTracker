from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from institutes.models import Institute, VisitedUsers
from usermanagement.models import CustomerProfile
from .serializers import (InstituitionSerializer, 
                            InstituitionRegistration, 
                            UserLoginSerializer, 
                            StaffSerializer, 
                            AddUserSerializer,
                            InstituiteProfileSerializer)
from django.contrib.auth.models import User

import firebase_admin
from firebase_admin import credentials
from datetime import datetime
from dateutil import parser
from firebase_admin import credentials, messaging

class StaffLogin(generic.View):

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            #route to home page


class StaffRegistration(generic.View):
    #create form
    pass


class HomePage(generic.TemplateView):
    pass


class PatientRegistration():
    pass


class PatientEdit():
    pass


class PatientDelete():
    pass


class GetInituitionList(APIView):
    model = Institute

    def get(self, request, *args, **kwargs):
        data = Institute.objects.all()
        print(type(data))
        return_data = InstituitionSerializer(data, many=True).data
        print(return_data)
        return Response(data={"instituite_list": return_data}, status=status.HTTP_200_OK)


class InstituteRegistration(generics.CreateAPIView):
    """ User Registration 
        params :
    """
    serializer_class = InstituitionRegistration

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=self.request.data)
    #     if not serializer.is_valid():
    #         return Response(
    #                 data={'response': serializer.errors},
    #                 status=status.HTTP_200_OK,
    #                 )
    #     else:
    #         self.perform_create(serializer)
    #         print(serializer.data, "seree")
    #         headers = self.get_success_headers(serializer.data)
    #         print('headers', headers, serializer.data['username'])
    #         user_obj = User.objects.get(username=serializer.data['username'])
    #         print(user_obj, type(serializer.data))
    #         token, _ = Token.objects.get_or_create(user=user_obj)
    #         headers = serializer.data
    #         headers['token'] = token
    #         headers['id'] = serializer.data['id']
    #         print("token, _", token, _)
    #         return Response(
    #                 data={'token':token.key},
    #                 headers=headers,
    #                 status=status.HTTP_200_OK,
    #                 )


class InstituitionLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            print("valid")
            staff_obj = serializer.get_profile()
            staff_data = StaffSerializer(staff_obj).data
            instituition_data = InstituitionSerializer(staff_obj.my_instituite).data
            token, _ = Token.objects.get_or_create(user=staff_obj.user)
            return Response(
                    data={'token':token.key,
                    'staff_data': staff_data,
                    'instituition_data': instituition_data},
                    status=status.HTTP_200_OK,
                    )
        else:
            print("Not valid", serializer.errors)
            return Response(
                    data={'token': None,
                    'staff_data': {}},
                    status=status.HTTP_200_OK,
                    )


def DetectUser(user):
    # import cv2
    # import os
    # import face_recognition
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # loc1 = str(BASE_DIR) + str(user.image.url)
    # # img = cv2.imread(loc1)
    # loc1 = os.path.abspath(loc1)
    # for each in CustomerProfile.objects.all():
    #     if each.profile_pic1:
    #         # print(each.id)
    #         loc2 =  str(BASE_DIR) + str(each.profile_pic1.url)
    #         loc2 = os.path.abspath(loc2)
    #         print("loc1", loc1)
    #         print("loc2", loc2)
    #         # loc1 = os.path.abspath("D:\Freelancer\Face_recognition-master\media\profile_pic\image_kNXo3Bw.jpeg")
    #         # # loc1 = r"F:/Photos/july2020.IMG-20191023-WA0016.jpg"
    #         # loc2 = os.path.abspath("D:/WhatsApp Image 2021-04-11 at 7.04.34 PM.jpeg")
    #         # face_1_image = face_recognition.load_image_file(loc2)
    #         # print(face_1_image)
    #         # face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

    #         # small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    #         # rgb_small_frame = small_frame[:, :, ::-1]

    #         # face_locations = face_recognition.face_locations(rgb_small_frame)
    #         # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    #         # check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
    #         known_image = face_recognition.load_image_file(loc1)
    #         unknown_image = face_recognition.load_image_file(loc2)

    #         # print("known_image", known_image)
    #         # print("unknown_image", unknown_image)

    #         biden_encoding = face_recognition.face_encodings(known_image)[0]
    #         unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    #         results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    #         print("results", results)
    #         if results[0]  == True:
    #             print("check", results)
    #             return True, each.user
    return  False, None


class AddVisitedUsers(generics.GenericAPIView):
    serializer_class = AddUserSerializer

    def post(self, *args, **kwargs):
        print(self.request.data)
        instituite_id = self.request.data.get('instituite')
        try:
            instituite = Institute.objects.get(id=instituite_id)
            user = VisitedUsers.objects.create(instituite=instituite, image=self.request.data['image'])
        except Exception  as e:
            print(e)
            return Response(
                data={'token': None,
                'staff_data': {},
                'msg': 'Invalid instituition Id.'},
                status=status.HTTP_200_OK,
                )
        else:
            status_, user_obj = DetectUser(user)
            print(status_, user_obj)
            if status_ == True:
                user.user = user_obj
                user.save()
                return Response(
                data={"msg": "User added successfully."},
                status=status.HTTP_200_OK,
                )
            else:
                return Response(
                data={"msg": "User npt found."},
                status=status.HTTP_200_OK,
                )


class SendAlert(APIView):

    def post(self, *args, **kwargs):
        print(self.request.data)
        institute_id = self.request.data.get("instituition_id")
        datetime_obj = parser.parse('2018-02-06T13:12:18.1278015Z')
        visited_users = VisitedUsers.objects.all()
        # FCM Push
        if not firebase_admin._apps:
            cred = credentials.Certificate("D:\Freelancer\Face_recognition-master\institutes\covitracker-6effa-firebase-adminsdk-g0e6o-f24a1dc3b5.json")
            firebase_admin.initialize_app(cred)
        print(visited_users, "ppp")
        # for each in visited_users:
        #     print(each)
        #     message = messaging.MulticastMessage(
        #         notification=messaging.Notification(
        #             title="Covid Alert!",
        #             body="You are requested to take home quarantine."
        #         ),
        #         data=None,
        #         tokens=[each.user.user_profile.fcm_token],
        #     )
        tokens = [each.user.user_profile.fcm_token for each in visited_users]
        import requests
        import json

        serverToken = 'AAAASIFtIsg:APA91bFAOFutVtI1AGowWxiNn4azwI265K1XOJOpjd2bOCngwKSXqfbOL_vU47-OxboRebttFgOuD9kI7gsVGdGZUl9gxx4SQvlP7jR9ubgblRmGrRuF9z8qkxDMv7-ZNKuBErhYt5Lq'
        deviceToken = ''

        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }
        for each in visited_users:
            print(each.user.user_profile.fcm_token)
            body = {
                    'notification': {'title': 'Sending push form python script',
                                        'body': 'New Message'
                                        },
                    'to': each.user.user_profile.fcm_token,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }

            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            print(response.status_code)

            print(response.json())

        return Response(data={}, status=status.HTTP_200_OK)


class InstituiteProfile(generics.RetrieveUpdateAPIView):
    serializer_class = InstituiteProfileSerializer
    queryset = Institute.objects.all()

    


#         {"date":"2021-04-11T05:41:00.000+0530",
# "id": "35"}