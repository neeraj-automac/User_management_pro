from rest_framework import serializers
from .models import *


# class User_Registration_Serializer(serializers.ModelSerializer):
#    class Meta:
#        model = User_registration
#        fields = ['name', 'category', 'mobile_num', 'email', 'location', 'age', 'gender']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(error_messages={
        'blank': ' password_field_cannot_be_blank.'
    })

    email = serializers.CharField(error_messages={
        'blank': 'username_field_cannot_be_blank.'
    })

    class Meta:
        model = User
        fields = ('email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)




class user_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = '__all__'


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']






# class User_create_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

class User_create_Serializer(serializers.ModelSerializer):
    # Additional fields for User_details
    name = serializers.CharField(max_length=50)
    contact_no = serializers.IntegerField()
    business_email = serializers.EmailField()
    location = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    gender = serializers.CharField(max_length=10)
    category = serializers.CharField(max_length=30)  # Assuming category is passed as an ID
    user_status=serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username',  'name', 'contact_no', 'business_email',
                  'location', 'age', 'gender', 'category','user_status']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Pop fields for User_details
        user_details_data = {
            'name': validated_data.pop('name'),
            'contact_no': validated_data.pop('contact_no'),
            'business_email': validated_data.pop('business_email'),
            'location': validated_data.pop('location'),
            'age': validated_data.pop('age'),
            'gender': validated_data.pop('gender'),
            'category': validated_data.pop('category'),
            'user_status':validated_data.pop('user_status')
        }

        # Create User
        user = User.objects.create_user(username=validated_data['username'], password="user@123")

        # Create User_details
        category = Category.objects.get(category=user_details_data.pop('category'))
        print("category____",category)

        User_details.objects.create(
            user_id=user,
            role="customer",
            category=category,

            **user_details_data
        )
        return user


class User_doj_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['date_joined']


class UserDetails_create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = ['user_id', 'name', 'contact_no', 'business_email', 'location', 'user_status','category']


class UserDetails_pagination_Serializer(serializers.ModelSerializer):
    # ----in order to access other model fileds in same serializer u need to use nested serializer here we have
    date_joined = serializers.DateTimeField(source='user_id.date_joined', read_only=True)

    # date_joined = User_doj_Serializer(many=True, read_only=True)
    # print('--------------------date_joined',date_joined)
    # name = serializers.CharField()
    # contact_no = serializers.IntegerField()
    # user_status = serializers.CharField()
    # business_email = serializers.EmailField()
    # location = serializers.CharField()

    class Meta:
        model = User_details
        fields = ['date_joined', 'name', 'contact_no', 'user_status', 'business_email', 'location']


class UserDetails_business_email_Serializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='users.username', read_only=True)

    class Meta:
        model = User_details
        fields = ['name', 'id']


class TemplateDetails_pagination_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ["id", "template_name", "template_heading", "template_body"]


class Template_dropdown_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ["id", "template_name"]


class Broadcast_Serializer(serializers.ModelSerializer):
    # In Django REST Framework, when you use serializers.SerializerMethodField(), it automatically looks for
    # a method in the serializer class named get_ < field_name >
    # In your case, since the field is named users, it looks for a method named get_users.so it is mandatory to name method as get_users
    # if not named in such a way it raises a attribute error as no get_users

    # fields = [,,,,,,]
    # fields = '__all__'

    template = serializers.CharField(source='template.template_name', read_only=True)
    # users = serializers.CharField(source='users.business_email', read_only=True)

    template_id = serializers.CharField(source='template.id', read_only=True)
    users = serializers.SerializerMethodField()
    frequency = serializers.CharField()
    follow_up = serializers.CharField()
    time = serializers.TimeField()
    sent_status = serializers.BooleanField()

    class Meta:
        model = Broadcast
        fields = ['id', 'template', 'template_id', 'users', 'frequency', 'follow_up', 'time', 'sent_status']

    def get_users(self, obj):
        # return [user.business_email for user in obj.users.all()]
        return [{'user_id': user.id, 'username': user.name} for user in obj.users.all()]


