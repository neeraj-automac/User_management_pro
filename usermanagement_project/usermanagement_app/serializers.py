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
        fields = [
            # Include all existing fields you need
            'user_id',
            'role',
            'name',
            'contact_no',
            'user_status',
            'category',
            'business_email',
            'location',
            'age',
            'gender',
            'how_did_you_learn_about_us',
            'type_of_challange',
            'goal',
            'date_of_joining',
            'height',
            'weight',
            'body_type',
            'blood_test',
            'bone_density',
            'body_fatpercentage',
            'muscle_mass',
            'any_physical_limitations',
            'any_concerns',
            'Total_attendance',
            'Total_water_intake',
            'Total_step_count',
            'Total_workout_duration',  # Optional: include raw duration
            'date_of_birth'        ]


# class user_details_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User_details
#         fields = '__all__'


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']






# class User_create_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

class User_create_Serializer(serializers.ModelSerializer):
    # Fields for User model
    username = serializers.CharField(max_length=150)

    # Additional fields for User_details
    name = serializers.CharField(max_length=50, allow_blank=True)
    contact_no = serializers.IntegerField(allow_null=True)
    business_email = serializers.EmailField(allow_blank=True)
    location = serializers.CharField(max_length=30, allow_blank=True)
    age = serializers.IntegerField(allow_null=True)
    gender = serializers.CharField(max_length=150, allow_blank=True)
    category = serializers.CharField(max_length=30)  # Assuming category is passed as a string (e.g., category name or ID)
    how_did_you_learn_about_us = serializers.CharField(max_length=500, allow_blank=True)
    type_of_challange = serializers.CharField(max_length=500, allow_blank=True)
    goal = serializers.CharField(allow_blank=True)
    date_of_joining = serializers.DateField(allow_null=True, default=None)
    height = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, default=None)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, default=None)
    body_type = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    blood_test = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    bone_density = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, default=None)
    body_fatpercentage = serializers.DecimalField(max_digits=4, decimal_places=1, allow_null=True, default=None)
    muscle_mass = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True, default=None)
    any_physical_limitations = serializers.CharField(allow_blank=True, allow_null=True)
    any_concerns = serializers.CharField(allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',  # User model field
            'name', 'contact_no', 'business_email', 'location', 'age', 'gender', 'category',
            'how_did_you_learn_about_us', 'type_of_challange', 'goal', 'date_of_joining',
            'height', 'weight', 'body_type', 'blood_test', 'bone_density', 'body_fatpercentage',
            'muscle_mass', 'any_physical_limitations', 'any_concerns','date_of_birth'
        ]
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
            'how_did_you_learn_about_us': validated_data.pop('how_did_you_learn_about_us'),
            'type_of_challange': validated_data.pop('type_of_challange'),
            'goal': validated_data.pop('goal'),
            'date_of_joining': validated_data.pop('date_of_joining'),
            'height': validated_data.pop('height'),
            'weight': validated_data.pop('weight'),
            'body_type': validated_data.pop('body_type'),
            'blood_test': validated_data.pop('blood_test'),
            'bone_density': validated_data.pop('bone_density'),
            'body_fatpercentage': validated_data.pop('body_fatpercentage'),
            'muscle_mass': validated_data.pop('muscle_mass'),
            'any_physical_limitations': validated_data.pop('any_physical_limitations'),
            'any_concerns': validated_data.pop('any_concerns'),
            'date_of_birth': validated_data.pop('date_of_birth', None),
        }

        # Create User
        user = User.objects.create_user(
            username=validated_data['username'],
            password="user@123"  # Consider making password configurable via the serializer
        )

        # Create User_details
        category = Category.objects.get(category=user_details_data.pop('category'))  # Assuming 'category' is a field in Category model
        User_details.objects.create(
            user_id=user,
            role="customer",
            category=category,
            user_status="active",
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
    username = serializers.DateTimeField(source='user_id.username', read_only=True)
    category=serializers.DateTimeField(source='category.category', read_only=True)
    # date_joined = User_doj_Serializer(many=True, read_only=True)
    # print('--------------------date_joined',date_joined)
    # name = serializers.CharField()
    # contact_no = serializers.IntegerField()
    # user_status = serializers.CharField()
    # business_email = serializers.EmailField()
    # location = serializers.CharField()

    class Meta:
        model = User_details
        fields = ['date_joined', 'name', 'contact_no', 'user_status', 'business_email', 'location','category','age','gender','username','how_did_you_learn_about_us',
'type_of_challange',
'goal',
'date_of_joining',
'height',
'weight',
'body_type',
'blood_test',
'bone_density',
'body_fatpercentage',
'muscle_mass',
'any_physical_limitations',
'any_concerns',
'Total_attendance',
'Total_water_intake',
'Total_step_count',
'Total_workout_duration','date_of_birth']


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
    category = serializers.SerializerMethodField()
    frequency = serializers.CharField()
    follow_up = serializers.CharField()
    time = serializers.TimeField()
    sent_status = serializers.BooleanField()

    class Meta:
        model = Broadcast
        fields = ['id', 'template', 'template_id', 'users', 'category','frequency', 'follow_up', 'time', 'sent_status']

    def get_users(self, obj):
        # return [user.business_email for user in obj.users.all()]
        return [{'user_id': user.id, 'username': user.name} for user in obj.users.all()]

    def get_category(self, obj):
        # return [user.business_email for user in obj.users.all()]
        return [{'category_id': cat.id, 'category': cat.category} for cat in obj.category.all()]



class category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category']


class challange_Serializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category', read_only=True)
    category_id = serializers.CharField(source='category.id', read_only=True)
    user_id = serializers.CharField(source='user_id.id', read_only=True)
    formatted_workout_duration = serializers.SerializerMethodField()

    # date_joined = serializers.DateTimeField(source='user_id.date_joined', read_only=True)

    class Meta:
        model = User_details
        fields = [
            'user_id',
            'name',
            'category',
            'category_id',
            'date_of_joining',
            'height',
            'weight',
            'body_type',
            'Total_attendance',
            'Total_water_intake',
            'Total_step_count',
            'Total_workout_duration',
            'goal',
            'formatted_workout_duration'
        ]

    def get_formatted_workout_duration(self, obj):
        return obj.get_formatted_duration()


class User_onboard_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = [
            'user_id',
            'name',
            'date_of_joining',
            'Total_attendance',
            'Total_water_intake',
            'Total_step_count',
            'Total_workout_duration',
            'goal'
        ]


class UserTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_tracking
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    # Use CharField for category if you're passing the category name
    category = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User_details
        fields = [
            'name', 'contact_no', 'business_email', 'location', 'age', 'gender',
            'category', 'how_did_you_learn_about_us', 'type_of_challange', 'goal',
            'date_of_joining', 'height', 'weight', 'body_type', 'blood_test',
            'bone_density', 'body_fatpercentage', 'muscle_mass',
            'any_physical_limitations', 'any_concerns', 'role', 'user_status',
            'Total_attendance', 'Total_water_intake', 'Total_step_count',
            'Total_workout_duration','date_of_birth'
        ]
        read_only_fields = ['user_id']  # Prevent updating the user_id field

    def update(self, instance, validated_data):
        # Handle category separately if provided
        category_data = validated_data.pop('category', None)
        if category_data:
            try:
                instance.category = Category.objects.get(category=category_data)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category": f"Category '{category_data}' does not exist."})

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance