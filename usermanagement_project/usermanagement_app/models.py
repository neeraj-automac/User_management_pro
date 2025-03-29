import datetime
from datetime import timedelta
from datetime import time
from django.contrib.postgres.fields import ArrayField
import requests
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.fields import EmailField
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Min, Max, Sum, Count, Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import json
import openpyxl
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from unicodedata import category


class Category(models.Model):
    category=models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.category

class User_details(models.Model):
    objects = models.Manager()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE )
    ROLE_STATUS_CHOICES = (('admin', 'admin'), ('customer', 'customer'))
    role = models.CharField(max_length=15, choices=ROLE_STATUS_CHOICES)
    name=models.CharField(max_length = 50,blank=True)#False
    contact_no = models.BigIntegerField(null=True, blank=True)#False,False
    user_status=models.CharField(max_length = 50,blank=True)#False
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    # company = models.CharField(max_length = 30,blank=True)#remove?
    business_email = models.EmailField(max_length = 254,blank=True)
    # years_of_experience = models.PositiveSmallIntegerField(null=True, blank=True)#remove?
    # job_position = models.CharField(max_length = 30,blank=True)#remove?
    location = models.CharField(max_length = 30,blank=True)#False
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=150,blank=True)
    how_did_you_learn_about_us=  models.CharField(max_length=500,blank=True)#False
    type_of_challange=  models.CharField(max_length=500,blank=True)#False
    goal=  models.TextField(blank=True)#False
    date_of_joining = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the person joined"
    )
    # Suitable for storing calendar dates; null=True needed with blank=True for proper DB handling

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height in centimeters (e.g., 175.50)"
    )
    # DecimalField good for precise measurements; max_digits=5 allows up to 999.99 cm

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight in kilograms (e.g., 70.50)"
    )
    # DecimalField for precise weight; max_digits=5 allows up to 999.99 kg

    body_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="E.g., ectomorph, mesomorph, endomorph"
    )
    # CharField for descriptive text; max_length=50 should be sufficient

    blood_test = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Blood test results or type"
    )
    # CharField as this could contain various formats of results

    bone_density = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Bone density measurement"
    )
    # DecimalField for numerical measurement with precision

    body_fatpercentage = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Body fat percentage (e.g., 22.5)"
    )
    # DecimalField; max_digits=4 allows 0.0-99.9%

    muscle_mass = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Muscle mass in kilograms"
    )
    # DecimalField for precise measurement

    any_physical_limitations = models.TextField(
        blank=True,
        null=True,
        help_text="Description of any physical limitations"
    )
    # TextField for longer descriptive text

    any_concerns = models.TextField(
        blank=True,
        null=True,
        help_text="Any health or other concerns"
    )

    Total_attendance=models.IntegerField(default=0,null=True,blank=True)
    Total_water_intake=models.FloatField(default=0.0,blank=True)
    Total_step_count=models.IntegerField(default=0,null=True, blank=True)
    Total_workout_duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.user_id.username

#
# class User_registration(models.Model):
#
#    name = models.CharField(max_length=100)
#    category = models.CharField(max_length=100)
#    mobile_num = models.BigIntegerField()
#    email = models.EmailField(unique=True)
#    location = models.CharField(max_length=100)
#    age = models.PositiveIntegerField()
#    gender = models.CharField(max_length=150)
#
#
#    def __str__(self):
#        return self.name

















#-----------------------hct models-----------------------

class Template(models.Model):

    template_name = models.CharField(max_length=50, blank=False)
    template_heading= models.CharField(max_length=100, blank=False)
    template_body=models.TextField()

    def __str__(self):
        return self.template_name






# class UserTemplateManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user_detail__user_status='active')


class Broadcast(models.Model):
    # user_detail = models.ForeignKey(User_details, on_delete=models.CASCADE)
    # user_template= models.ForeignKey(Template, on_delete=models.CASCADE)
    template=models.ForeignKey(Template, on_delete=models.CASCADE)
    # users=models.ManyToManyField(User_details,blank=True)
    users = models.ManyToManyField(User_details, blank=True)
    category = models.ManyToManyField(Category, blank=True)

    frequency=models.CharField(max_length=150)
    follow_up=models.CharField(max_length=50,blank=False)
    time=models.TimeField(null=True, blank=True)
    sent_status=models.BooleanField(default=False)




    # objects = UserTemplateManager()
    #
    # def save(self, *args, **kwargs):
    #
    #     # if self.user_detail.user_status != 'active':
    #     #     raise ValidationError('User must be active to be included in UserTemplate.')
    #     # super().save(*args, **kwargs)
    #     if self.user_detail.user_status != 'active':
    #         logger.warning(f'Attempted to save UserTemplate for inactive user: {self.user_detail.user_id.username}')
    #         return  # Skip saving the instance
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.follow_up










@receiver(post_save, sender=Broadcast)
def send_broadcast(sender, instance, created, **kwargs):
    if created:
        print("created")


    else:
        print("edited in models.py")
        if instance.sent_status==True:
            def mail_field():
                print("broadcast_usersssss", instance.users.all())
                email_addresses = list(instance.users.values_list('business_email', flat=True))
                print("User email addresses:", email_addresses, type(email_addresses))
                # contact_numbers = list(instance.users.values_list('contact_no', flat=True))
                # print("User contact_numbers:", contact_numbers, type(contact_numbers))
                print(instance.template.template_name)
                print(instance.template.template_heading)
                print(instance.template.template_body)
                print("sending once via mail")
                send_mail(instance.template.template_heading, '', from_email=settings.EMAIL_HOST_USER,
                          recipient_list=email_addresses, html_message=instance.template.template_body)
                print("sended")

            def mail_category():
                category_users=User_details.objects.filter(category=instance.category)
                print('category_users',category_users)
                email_addresses = list(category_users)
                print("User email addresses:", email_addresses, type(email_addresses))
                # contact_numbers = list(instance.users.values_list('contact_no', flat=True))
                # print("User contact_numbers:", contact_numbers, type(contact_numbers))
                print(instance.template.template_name)
                print(instance.template.template_heading)
                print(instance.template.template_body)
                print("sending once via mail")
                send_mail(instance.template.template_heading, '', from_email=settings.EMAIL_HOST_USER,
                          recipient_list=email_addresses, html_message=instance.template.template_body)
                print("sended")
                pass

            def whatsapp_user_num_list():
                print("Sending messages via WhatsApp...")
                try:
                    num_list = list(instance.users.values_list('contact_no', flat=True))
                    print(f"Numbers to process: {num_list}")

                    responses = []  # To store responses for each number

                    for number in num_list:
                        url = "https://graph.facebook.com/v21.0/422738437582013/messages"
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "to": number,
                            "type": "template",
                            "template": {
                                "name": "hello_world",
                                "language": {
                                    "code": "en_US"
                                }
                            }
                        })
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer EAAMY4TVLDQ4BO3ssWkoDE02RvTuYfCsH6E1khXZCY2h4bfdZCrS6nCnZAZBwEmAZCHdvWCxCAwt9ZBZA8HhaZCyQDgH2zjEPowuZCcOBzher6O31DyiaDFijfigjyBzEoIr8o1ZClBLsTKZACjZCYxndOuGnc8VCO5X11Ci4QFZCB6g8UV0zfVXG43itf2CciVbA6ZA5gZCu5pnc8vmtBf8russDSqsRdxZBnBUZD'
                        }

                        response = requests.post(url, headers=headers, data=payload)
                        print(f"Response for {number}: {response.status_code}, {response.text}")
                        responses.append({
                            "number": number,
                            "status_code": response.status_code,
                            "response": response.json() if response.status_code == 200 else response.text
                        })

                        if response.status_code != 200:
                            print(f"Failed to send message to {number}: {response.status_code}")

                    # Log or return all responses after the loop completes
                    print("All responses:", responses)
                    return JsonResponse({"responses": responses}, safe=False)

                except Exception as e:
                    print(f"Error occurred: {e}")
                    return JsonResponse({'error': str(e)})

            def whatsapp_category_num_list():
                category_contact_numbers = User_details.objects.filter(category=instance.category).values_list('contact_no', flat=True)
                # print('category_users', category_users)
                # contact_numbers = list(category_users)
                print("User contact_numbers:", category_contact_numbers, type(category_contact_numbers))
                # contact_numbers = list(instance.users.values_list('contact_no', flat=True))
                # print("User contact_numbers:", contact_numbers, type(contact_numbers))
                print("Sending messages via WhatsApp...")
                try:
                    # num_list = list(instance.users.values_list('contact_no', flat=True))
                    # print(f"Numbers to process: {num_list}")

                    responses = []  # To store responses for each number

                    for number in category_contact_numbers:
                        url = "https://graph.facebook.com/v21.0/422738437582013/messages"
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "to": number,
                            "type": "template",
                            "template": {
                                "name": "hello_world",
                                "language": {
                                    "code": "en_US"
                                }
                            }
                        })
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer EAAMY4TVLDQ4BOyMBcLQ2wq0RxZBgeGo79J5Bb2h60Dl4TZC0ZCkZCLVHKknfilC33NQ6NKZBxXEFLc54t4j0PXjdLZCC9QPgTmYK6GZAROheDPwU9OZACsITQpKH8tyxN4YbsF6V4QTHciDJxRruu0eks5gujLJyCHKlceMfXFb0aa2240KsZCWHGpY7cZCQKPQHAEIykjnqFtT4cvTvuue5LJcL8IJtEZD'
                        }

                        response = requests.post(url, headers=headers, data=payload)
                        print(f"Response for {number}: {response.status_code}, {response.text}")
                        responses.append({
                            "number": number,
                            "status_code": response.status_code,
                            "response": response.json() if response.status_code == 200 else response.text
                        })

                        if response.status_code != 200:
                            print(f"Failed to send message to {number}: {response.status_code}")

                    # Log or return all responses after the loop completes
                    print("All responses:", responses)
                    return JsonResponse({"responses": responses}, safe=False)

                except Exception as e:
                    print(f"Error occurred: {e}")
                    return JsonResponse({'error': str(e)})



            # email_body = f'''<p>instance.template.template_heading</p>'''
            if instance.frequency == "once" and instance.follow_up == "mail" and instance.users.exists():
                print("once, mail, instance.users")
                mail_field()

            elif instance.frequency == "periodically" and instance.follow_up == "mail" and instance.users.exists():
                # mail_field()
                print("periodically, mail, instance.users")


            elif instance.frequency == "once" and instance.follow_up == "mail" and instance.category is not None:
                print("once, mail, instance.category")
                mail_category()

            elif instance.frequency == "periodically" and instance.follow_up == "mail" and instance.category is not None:
                print("periodically, mail, instance.category")
                # mail_category()


            elif instance.frequency == "once" and instance.follow_up == "whatsapp" and instance.users.exists():
                print("once, whatsapp, instance.users")
                whatsapp_user_num_list()

            elif instance.frequency == "periodically" and instance.follow_up == "whatsapp" and instance.users.exists():
                print("periodically, whatsapp, instance.users")
                # whatsapp_user_num_list()


            elif instance.frequency == "once" and instance.follow_up == "whatsapp" and instance.category is not None:
                print("once, whatsapp, instance.category")
                whatsapp_category_num_list()

            elif instance.frequency == "periodically" and instance.follow_up == "whatsapp" and instance.category is not None:
                print("periodically, whatsapp, instance.category")
                # whatsapp_category_num_list()


            elif instance.frequency == "once" and instance.follow_up == "both" and instance.users.exists():
                pass

            elif instance.frequency == "periodically" and instance.follow_up == "both" and instance.users.exists():
                pass

            elif instance.frequency == "once" and instance.follow_up == "both" and instance.category is not None:
                pass

            elif instance.frequency == "periodically" and instance.follow_up == "both" and instance.category is not None:
                pass

            else:
                print("something else ")

        else:
            print("executing -sent status is False")
    # else:
    #     print("not created not updated")





# @receiver(post_save, sender=User_registration)
# @receiver(post_save, sender=User)
# def send_broadcast(sender, instance, created, **kwargs):
#     if created:
#         # user = User.objects.create_user(username=instance.name, password="user@123")
#         user = instance.username
#         # print(user.is_staff)
#         # user.save()
#         # user_details = User_details.objects.create(user_id=user,role="customer",name=instance.name,contact_no=instance.mobile_num,user_status="",company="",business_email=instance.email,years_of_experience=None,job_position="",location=instance.location,age=instance.age,gender=instance.age,category=instance.category)
#         user_details = User_details.objects.create(user_id=user,role="customer",name=instance.name,contact_no=instance.mobile_num,user_status="active",business_email=instance.email,location=instance.location,age=instance.age,gender=instance.gender,category=instance.category)
#         user_details.save()
#         print('user_created')
#         print("created in user_reg")
#
#
#
#     else:
#
#         print("edited in user reg models.py")



#
# class BulkUserUploadView(APIView):
#     permission_classes = [permissions.AllowAny]  # Adjust based on requirements
#
#     def post(self, request, *args, **kwargs):
#         file = request.FILES.get('file')  # Expecting an Excel file
#         if not file:
#             return JsonResponse({"error": "No file uploaded"}, status=400)
#
#         try:
#             wb = openpyxl.load_workbook(file)
#             sheet = wb.active  # Get the first sheet
#
#             users_created = []
#             errors = []
#
#             # Assuming the Excel file has headers:
#             # ["username", "name", "contact_no", "business_email", "location", "age", "gender", "category", "user_status"]
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 username, name, contact_no, business_email, location, age, gender, category_name, user_status = row
#
#                 # Validate required fields
#                 if not all([username, name, contact_no, business_email, location, age, gender, category_name, user_status]):
#                     errors.append({"row": row, "error": "Missing required fields"})
#                     continue
#
#                 # Validate category existence
#                 try:
#                     category = Category.objects.get(category=category_name)  # Adjust field name if necessary
#                 except Category.DoesNotExist:
#                     errors.append({"row": row, "error": f"Category '{category_name}' not found"})
#                     continue
#
#                 # Prepare user data
#                 user_data = {
#                     "username": username,
#                     "name": name,
#                     "contact_no": contact_no,
#                     "business_email": business_email,
#                     "location": location,
#                     "age": age,
#                     "gender": gender,
#                     "category": category.id,  # Use category ID
#                     "user_status": user_status
#                 }
#
#                 # Validate and save user using the serializer
#                 serializer = User_create_Serializer(data=user_data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     users_created.append(username)
#                 else:
#                     errors.append({"row": row, "error": serializer.errors})
#
#             return JsonResponse(
#                 {"message": "User creation completed", "users_created": users_created, "errors": errors},
#                 status=status.HTTP_201_CREATED
#             )
#
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#
# class User_details(models.Model):
#     objects = models.Manager()
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE )
#     ROLE_STATUS_CHOICES = (('admin', 'admin'), ('customer', 'customer'))
#     role = models.CharField(max_length=15, choices=ROLE_STATUS_CHOICES)
#     name=models.CharField(max_length = 50,blank=False)
#     contact_no = models.BigIntegerField(null=False, blank=False)
#     user_status=models.CharField(max_length = 50,blank=True)
#     category=models.ForeignKey(Category, on_delete=models.CASCADE)
#     # company = models.CharField(max_length = 30,blank=True)#remove?
#     business_email = models.EmailField(max_length = 254,blank=False)
#     # years_of_experience = models.PositiveSmallIntegerField(null=True, blank=True)#remove?
#     # job_position = models.CharField(max_length = 30,blank=True)#remove?
#     location = models.CharField(max_length = 30,blank=False)
#     age = models.PositiveIntegerField()
#     gender = models.CharField(max_length=150)
#     how_did_you_learn_about_us=  models.CharField(max_length=500,blank=False)
#     type_of_challange=  models.CharField(max_length=500,blank=False)
#     goal=  models.TextField(blank=False)
#     # otp = models.CharField(max_length=255, unique=True, blank=True, null=True)
#     # course_id=models.IntegerField(null=True, blank=True)
#
#
#
#
#     def __str__(self):
#         return self.user_id.username



class User_tracking(models.Model):
    objects = models.Manager()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE )
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    date_of_activity=models.DateField()
    day_count = models.IntegerField(null=True, blank=True)#False,False
    step_count = models.IntegerField(null=True, blank=True)#False,False
    diet=models.JSONField(blank=True)
    Exercises = models.TextField(blank=True)
    water_in_liters = models.FloatField(blank=True)
    hours_of_sleep=  models.TimeField(blank=True)#False
    workout_duration=  models.TimeField(blank=True)#False
    calories_initial=  models.FloatField(blank=True)#False
    calories_burn= models.FloatField(blank=True)#False
    just_relief_activity=  models.CharField(max_length=500,blank=True)#False

    def __str__(self):
        return self.user_id.username






@receiver(post_save, sender=User_tracking)
def update_user_details_totals(sender, instance, created, **kwargs):
    user = instance.user_id  # Get the related user

    # Calculate sums for numeric fields
    totals = User_tracking.objects.filter(user_id=user).aggregate(
        total_water=Coalesce(Sum('water_in_liters'), 0.0),
        total_attendance=Count('id'),
        total_step_count=Coalesce(Sum('step_count'), 0),
    )

    # Handle TimeField aggregation (convert to seconds, sum, then convert back)
    workout_durations = User_tracking.objects.filter(user_id=user).values_list('workout_duration', flat=True)
    total_seconds = sum((t.hour * 3600 + t.minute * 60 + t.second) if t else 0 for t in workout_durations)
    total_workout_duration = timedelta(seconds=total_seconds)
    # user_details.Total_workout_duration = total_workout_duration

    # Get or create the corresponding User_details record
    user_details, _ = User_details.objects.get_or_create(user_id=user)

    # Update fields in User_details
    user_details.Total_water_intake = totals['total_water']
    user_details.Total_attendance = totals['total_attendance']
    user_details.Total_step_count = totals['total_step_count']
    user_details.Total_workout_duration = total_workout_duration
    user_details.save()


