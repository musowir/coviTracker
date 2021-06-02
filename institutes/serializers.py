from rest_framework import serializers
from django.core import validators
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.core.validators import validate_email
from rest_framework.validators import UniqueTogetherValidator

from usermanagement.models import CustomerProfile
from institutes.models import Institute, StaffProfile, VisitedUsers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class InstituitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = "__all__"


class InstituitionRegistration(serializers.ModelSerializer):

    # Instituition Details
    name = serializers.CharField(required=True, label="Instituition Name")
    contact_no = serializers.CharField(required=True, label="Contact no.")
    email = serializers.CharField(source='staff.user.email', required=True, validators=[])

    username = serializers.CharField(source='staff.user.username', required=True, label="Staff Username")
    first_name = serializers.CharField(source='staff.user.first_name', required=True)
    last_name = serializers.CharField(source='staff.user.last_name', required=True)
    password = serializers.CharField(source='staff.user.password', required=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj.staff.user)
        return token.key

    class Meta:
        model = Institute
        fields = ('name', 'contact_no', 'email', 'location', 'image', 
                'username', 'first_name', 'last_name', 'password', 'id', 'token')

    def validate(self, attrs):
        print(attrs)
        user_data = attrs['staff']['user']
        if User.objects.filter(username=user_data.get("username")).exists():
            raise serializers.ValidationError("Username already exists!.")
        else:
            return attrs
        

    def create(self, validated_data):
        user_obj = User.objects.create(first_name=validated_data['staff']['user']['first_name'], last_name=validated_data['staff']['user']['last_name'], username=validated_data['staff']['user']['username'], email=validated_data['staff']['user']['email'])
        # print(validated_data['user']['password'])
        user_obj.set_password(validated_data['staff']['user']['password'])
        user_obj.save()
        staff = StaffProfile.objects.create(user=user_obj, profile_pic="", mobile=validated_data['contact_no'])
        profile_obj = Institute.objects.create(staff=staff, image=validated_data.get('image'), 
                        location=validated_data['location'], contact_no=validated_data['contact_no'], 
                        name=validated_data['name'])
        return profile_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_username': 'Invalid username.',
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        if not User.objects.filter(username=attrs.get("username")).exists():
            raise serializers.ValidationError(self.default_error_messages['inactive_username'])
        elif not authenticate(username=attrs.get("username"), password=attrs.get('password')):
            raise serializers.ValidationError(self.default_error_messages['invalid_credentials'])
        else:
            self.user_obj = User.objects.get(username=attrs.get("username"))
            return attrs

    def get_profile(self):
        staff_profile = StaffProfile.objects.get(user=self.user_obj)
        return staff_profile


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProfile
        fields = "__all__"


class AddUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    
    class Meta:
        model = VisitedUsers
        fields = "__all__"


class InstituiteProfileSerializer(serializers.ModelSerializer):
    # Instituition Details
    name = serializers.CharField(required=True, label="Instituition Name")
    contact_no = serializers.CharField(required=True, label="Contact no.")
    email = serializers.CharField(source='staff.user.email', required=True, validators=[])

    # username = serializers.CharField(source='staff.user.username', required=True, label="Staff Username")
    first_name = serializers.CharField(source='staff.user.first_name', required=True)
    last_name = serializers.CharField(source='staff.user.last_name', required=True)
    password = serializers.CharField(source='staff.user.password', required=True)
    
    class Meta:
        model = Institute
        fields = ("id", "name", "contact_no", "location", "email", "image", 
                "first_name", "last_name", "password")

    def update(self, instance, validated_data):
        instance.staff.user.first_name = validated_data['staff']['user'].get('first_name', instance.staff.user.first_name)
        instance.staff.user.last_name = validated_data['staff']['user'].get('last_name', instance.staff.user.last_name)
        instance.staff.user.email = validated_data['staff']['user'].get('email', instance.staff.user.email)
        if validated_data['staff']['user'].get('password'):
            instance.staff.user.set_password(validated_data['staff']['user'].get('password'))
            instance.staff.user.save()
        instance.name = validated_data.get('name', instance.name)
        instance.contact_no = validated_data.get('name', instance.contact_no)
        instance.location = validated_data.get('location', instance.image)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance