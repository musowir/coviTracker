from rest_framework import serializers
from django.core import validators
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.core.validators import validate_email
from rest_framework.validators import UniqueTogetherValidator

from usermanagement.models import CustomerProfile, UserFeedback
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


alphanumeric = validators.RegexValidator(r'^[0-9_a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
alphaspecial = validators.RegexValidator(r'^[ .a-zA-Z+-]*$', 'Only characters along with " + - " are allowed.')
characters_only = validators.RegexValidator(r'^[a-zA-Z_]*$', 'Only characters are allowed.')
character_special = validators.RegexValidator(r"^[' .0-9_a-z_A-Z_',:]*$", 'Please enter a valid character.')
decimal_only = validators.RegexValidator(r"^[0-9]+\.?[0-9]+$", 'Please enter a valid decimal.')
phone_number_validator = validators.RegexValidator(r"^[ .0-9+]+$", 'Please enter a valid phone number.')


class CustomerProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source='user.email', required=True, validators=[])
    password = serializers.CharField(source='user.password', write_only=True, required=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    name = serializers.CharField(required=False)
    token = serializers.SerializerMethodField()
    covid_status = serializers.SerializerMethodField()

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj.user)
        return token.key

    def get_covid_status(self, obj):
        return obj.get_covid_status_display()

    class Meta:
        model = CustomerProfile
        fields = ('id', 'phone_number',"name", 'email', 'gender', 
                    'first_name', 'last_name', 'password', 'otp_verified', 
                    'profile_pic1', 'profile_pic2', 'profile_pic3', 'token', 'fcm_token', 'covid_status')
        # extra_kwargs = {'first_name': {'required': False}}

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(CustomerProfileSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Id already exists")
        return value
    
    def validate_phone_number(self, value):
        if CustomerProfile.objects.filter(phone_number=value).exists() or User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        print(validated_data, "validated_data")
        user_obj = User.objects.create(first_name=validated_data['name'], username=validated_data['phone_number'], email=validated_data['user']['email'])
        user_obj.set_password(validated_data['user']['password'])
        user_obj.save()
        profile_obj = CustomerProfile.objects.create(user=user_obj, gender=validated_data.get('gender'), phone_number=validated_data['phone_number'], 
                profile_pic1=validated_data['profile_pic1'], profile_pic2=validated_data.get('profile_pic2'), profile_pic3=validated_data.get('profile_pic3'), 
                fcm_token=validated_data['fcm_token'])
        return profile_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # default_error_messages = {
    #     'inactive_account': _('User account is disabled.'),
    #     'invalid_credentials': _('Unable to login with provided credentials.')
    # }

    default_error_messages = {
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }
    
    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        phone_ = False
        email_ = False
        if User.objects.filter(username=attrs.get("username")).exists():
            phone_ = True
        elif User.objects.filter(email=attrs.get("username")).exists() and User.objects.filter(email=attrs.get("username")).count() == 1:
            username = User.objects.get(email=attrs.get("username")).username
            email_ = True
        if phone_ or email_:
            if phone_:
                self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
            else:
                self.user = authenticate(username=username, password=attrs.get('password'))
            if self.user:
                if not self.user.is_active:
                    raise serializers.ValidationError(self.error_messages['inactive_account'])
                return attrs
            else:
                raise serializers.ValidationError(self.error_messages['invalid_credentials'])
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    # Instituition Details
    # name = serializers.CharField(required=True, label="Instituition Name")
    phone_number = serializers.CharField(required=False, label="Phone Number", validators=[UniqueValidator(queryset=CustomerProfile.objects.all(), lookup='iexact')])
    email = serializers.CharField(source='user.email', required=False, validators=[])

    # username = serializers.CharField(source='user.username', required=True, label="Staff Username")
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    password = serializers.CharField(source='user.password', required=False)
    
    class Meta:
        model = CustomerProfile
        fields = ("id", "first_name", "last_name", "phone_number", "email", "password")

    def update(self, instance, validated_data):
        print('validated_data', validated_data)
        if validated_data.get('phone_number') and User.objects.filter(username=validated_data.get('phone_number')).exclude(username=instance.user.username).exists():
            print("username not exists")
            raise serializers.ValidationError("Username already exists!.")
        else:
            instance.user.username = validated_data.get('phone_number', instance.user.username)
            instance.user.first_name = validated_data['user'].get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data['user'].get('last_name', instance.user.last_name)
            instance.user.email = validated_data['user'].get('email', instance.user.email)
            if validated_data['user'].get('password'):
                instance.user.set_password(validated_data['user'].get('password'))
                instance.user.save()
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.profile_pic1 = validated_data.get('profile_pic1', instance.profile_pic1)
            instance.save()
            return instance


class UserFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFeedback
        fields = ("customer", "feedback")