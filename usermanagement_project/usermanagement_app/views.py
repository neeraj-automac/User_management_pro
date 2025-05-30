from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
import random
from django.db.models import Q,Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from . import models
from .models import *
import ast
from rest_framework.renderers import JSONRenderer
from django.core import serializers as core_serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core import serializers
import json
from datetime import datetime, time, timedelta,date
from django.conf import settings
from django.db.models import Min, Max
from functools import reduce
from django.core.paginator import Paginator
# Create your views here.
# @api_view(['GET'])
# def all_users_status(request):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # if request.user.is_authenticated:
#     if request.method == 'GET':
#         gold_category = Category.objects.get(category="gold")  # Get ID for "gold"
#         silver_category = Category.objects.get(category="silver")
#         all_users = User_details.objects.filter(Q(category=gold_category) | Q(category=silver_category))
#         total_user_count = len(all_users)
#
#         print('all_users', all_users)
#         active_users = User_details.objects.filter(category=gold_category).count()
#         print('active_users', active_users)
#         inactive_users = User_details.objects.filter(category=silver_category).count()
#         print('inactive_users', inactive_users)
#
#         # print("read the record")
#             {"status": {"total_users": total_user_count, "gold": active_user
#
#         return JsonResponse(s, "silver": inactive_users}})
#     # else:
#     #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['GET'])
def all_users_status(request):
    if request.method == 'GET':
        # Get all categories and their user count
        category_counts = (
            # User_details.objects.values('category__category')
            # .annotate(count=Count('id'))
            User_details.objects.filter(user_status="active")
            .values('category__category')
            .annotate(count=Count('id'))
        )

        total_user_count = sum(item['count'] for item in category_counts)

        category_data = [{"category": item['category__category'], "count": item['count']} for item in category_counts]

        return JsonResponse({"status": {"total_users": total_user_count, "categories": category_data}})


# hct
@api_view(["DELETE"])
def delete_users(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    # if request.method == 'POST':
    #     serializer = User_create_Serializer(data={"username":request.data.get("email"),"password":"user@123"})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse({"status": "user_registered_successfully"})
    #     return JsonResponse(serializer.errors)
        # # username_for_user_table = request.data.get('business_email')
        # # before_at_the_rate_part, domain = username_for_user_table.split("@")
        # # final_username_for_user_table = f"{before_at_the_rate_part}_hct@{domain}"
        # final_username_for_user_table=request.data.get('business_email')
        # print('*********', final_username_for_user_table)
        # print(request.data)
        # user_create_Serializer = User_create_Serializer(data={"username": final_username_for_user_table,
        #                                                       "password": "user@123"})  # request.data.get('password')
        # # User.objects.get
        # # new_user=User.objects.create(username="neerajpynam@gmail.com",password="Neeraj@584")
        # # new_user.save()
        # # new_user_details=User_details.objects.create(user_id_id="neerajpynam@gmail",name="neeru",contact_no=123456789,business_email="neerajpynam@gmail.com",location="hyd")
        # # new_user_details.save()
        #
        # if user_create_Serializer.is_valid():
        #     created_user = user_create_Serializer.save()
        #     userdetails_create_Serializer = UserDetails_create_Serializer(
        #         data={"user_id": created_user.pk, "name": request.data.get('name'),
        #               "contact_no": request.data.get('contact_no'),
        #               "business_email": request.data.get('business_email'),
        #               "location": request.data.get('location'), "user_status": request.data.get('user_status'),"category":request.data.get('category')})
        #
        #     if userdetails_create_Serializer.is_valid():
        #         userdetails_create_Serializer.save()
        #         return JsonResponse({"status": "created"})
        #
        #     else:
        #         print('ud', userdetails_create_Serializer.errors)
        #
        # else:
        #     print('errors------------', user_create_Serializer.errors)

    if request.method == "DELETE":

        try:
            user_to_be_deleted = User_details.objects.get(business_email=request.query_params.get("business_email"))
            # if user_to_be_deleted is not None:
            final_delete_usr = user_to_be_deleted.user_id
            final_delete_usr.delete()
            return JsonResponse({"status": "user_deleted_sucessfully"})
            # else:
            #     return JsonResponse({"status": "userdoesnot exist"})

        except User_details.DoesNotExist:
            return JsonResponse({"status": "user_does_not_exist"})
    else:
        return JsonResponse({"status": "not_post_not_delete"})
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# hct user tabel pagination
# @api_view(['GET'])
# def pagination(request):
#     # if request.user.is_authenticated:
#     if request.method=="GET":
#         if int(request.query_params.get("page"))>0:
#             #username,contact,email,dateofjoin,location
#             # contact_list = User_details.objects.all().order_by('-id')
#             contact_list = User_details.objects.filter(user_id__username__contains='_hct').order_by('-id')
#             print('contact_list',contact_list)
#
#             user_details_rec_serializer=UserDetails_pagination_Serializer(contact_list,many=True)
#             print('user_details_rec_serializer',user_details_rec_serializer)
#             print('user_details_rec_serializer_data',user_details_rec_serializer.data)
#
#
#             paginator = Paginator(user_details_rec_serializer.data,30)  # Show 25 contacts per page.
#             print('paginator',paginator)
#
#
#             page_number = request.query_params.get("page")
#             page_obj = paginator.get_page(page_number)
#             print("number of pages",paginator.num_pages,page_obj)
#             # print("next page",page_obj.next_page_number())
#             # print("previous_page_number",page_obj.previous_page_number()())
#             page_serializer = UserDetails_pagination_Serializer(page_obj, many=True)
#             print("page_serializer.data",page_serializer.data)
#
#             return JsonResponse({"number_of_pages":paginator.num_pages,"page_obj": page_serializer.data})
#             # return JsonResponse({"number_of_pages":"yo"})
#         else:
#             return JsonResponse({"status":"invalid_page_number"})
#     else:
#         return JsonResponse({"status": "not get req"})
#
#     # else:
#     #     return JsonResponse({"status": "unauthorized_user"})

@api_view(['GET'])
def pagination(request):
    if request.method == "GET":
        page_number = request.query_params.get("page", 1)
        page_size = 10  # Match page size with user_challenge_records_pagination

        # Validate page number
        try:
            page_number = int(page_number)
            if page_number < 1:
                return JsonResponse({"status": "invalid_page_number"}, status=200)
        except ValueError:
            return JsonResponse({"status": "invalid_page_number"}, status=200)

        # Get the list of contacts
        contact_list = User_details.objects.all().order_by('-id')

        # Paginate the queryset
        paginator = Paginator(contact_list, page_size)
        total_contacts = paginator.count  # Total number of records
        total_pages = paginator.num_pages  # Total number of pages

        # Get the page object
        try:
            page_obj = paginator.page(page_number)
        except:
            return JsonResponse({"status": "page_not_found"}, status=200)

        # Serialize the paginated data
        page_serializer = UserDetails_pagination_Serializer(page_obj, many=True)

        # Calculate next and previous pages
        next_page = page_number + 1 if page_obj.has_next() else None
        previous_page = page_number - 1 if page_obj.has_previous() else None

        # Construct response
        response = {
            "number_of_pages": total_pages,
            "current_page": page_number,
            "next_page": next_page,
            "previous_page": previous_page,
            "page_obj": page_serializer.data
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)


# hct
@api_view(['PUT'])
def update_user_status(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    if request.method == "PUT":
        print("inside putt")
        print(request.data.get("business_email"))
        try:
            # user_pk=User.objects.get(username=request.data.get("username")).pk
            user_status_to_be_updated = User_details.objects.get(business_email=request.data.get("business_email"))
            # print('00000',user_status_to_be_updated.user_status)
            if user_status_to_be_updated.user_status == "inactive":
                print("inactive")
                user_status_to_be_updated.user_status = "active"
                user_status_to_be_updated.save()
                print("active", user_status_to_be_updated.user_status)
                return JsonResponse({"status": "user_status_inactive_to_active_updated_sucessfully"})
            elif user_status_to_be_updated.user_status == "active":
                print("active")
                user_status_to_be_updated.user_status = "inactive"
                user_status_to_be_updated.save()
                print("inactive", user_status_to_be_updated.user_status)

                return JsonResponse({"status": "user_status_active_to_inactive_updated_sucessfully"})
            else:
                print("something else")






        except User.DoesNotExist:
            return JsonResponse({"status": "user_does_not_exist"})


    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# hct
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Optional: restrict to authenticated users
def edit_user_details_hct(request):
    try:
        # Get the User instance by username
        business_email=request.data.get("business_email")

        # Get the associated User_details instance
        user_details = User_details.objects.get(business_email=business_email)

    except User_details.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "User details not found."}, status=200)

    if request.method == 'PUT':
        serializer = UserDetailsSerializer(user_details, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "user_details_updated_successfully"}, status=200)
        return JsonResponse({"status": "failed", "errors": serializer.errors}, status=200)

    return JsonResponse({"status": "failed", "error": "Only PUT requests are allowed."}, status=200)


# hct
@api_view(['PUT'])
def broadcast(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    print(request.data)
    # print(request.user)
    # a=User.objects.get(username='neerajpynam3@gmail.com')
    # a=request.data
    # template = request.data.get('template')
    # type=request.data.get("type")
    # type=request.data.get("type")
    # ut=UserTemplate.objects.get(template__template_name=template)
    # print(ut.template.template_name)
    # print(ut.template.template_heading)
    # print(ut.template.template_body)

    broadcast_user = Broadcast.objects.get(id=request.data.get('broadcast_id'))
    broadcast_user.sent_status = True
    broadcast_user.save()
    # print("broadcast_user ",broadcast_user)
    # print("broadcast_user frequency",broadcast_user.frequency)
    # print("broadcast_usersssss",broadcast_user.users.all())
    # email_addresses = list(broadcast_user.users.values_list('user_id__username', flat=True))
    # print("User email addresses:",email_addresses,type(email_addresses))
    # contact_numbers = list(broadcast_user.users.values_list('contact_no', flat=True))
    # print("User contact_numbers:", contact_numbers,type(contact_numbers))
    # print(broadcast_user.template.template_name)
    # print(broadcast_user.template.template_heading)
    # print(broadcast_user.template.template_body)

    return JsonResponse({'status': 'sent successfully'})
    # return JsonResponse({"status":"Please_provide_valid_email"})
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# hct
@api_view(['GET'])
def hct_active_users(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    active_users_list = []
    if request.method == 'GET':
        active_users = User_details.objects.filter(user_status='active')
        print('active_users', active_users, type(active_users))
        active_users_serializer = UserDetails_business_email_Serializer(active_users, many=True)
        print(active_users_serializer)
        active_users_serializer_data = active_users_serializer.data
        print('//////////////', active_users_serializer_data)

        active_users_list = [{'user_id': user['id'], 'name': user['name']} for user in
                             active_users_serializer_data]

        return JsonResponse({"active_users": active_users_list})
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['POST'])
#
def create_template(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    data = request.data
    print("data", data)
    try:
        template_exists = Template.objects.get(template_name=request.data.get('template_name'))
        return JsonResponse({"status": "Template_exists"})


    except Template.DoesNotExist:
        new_template = Template.objects.create(template_name=request.data.get('template_name'),
                                               template_heading=request.data.get('template_heading'),
                                               template_body=request.data.get('template_body'))
        new_template.save()
        return JsonResponse({"status": "Template_added_successfully"})
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['PUT'])
def update_template(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    data = request.data
    print("data", data)
    try:

        template = Template.objects.get(id=request.data.get('template_id'))
        if template is not None:
            print(template.template_name)
            template.template_name = request.data.get('template_name')
            template.template_heading = request.data.get('template_heading')
            template.template_body = request.data.get('template_body')
            template.save()

            return JsonResponse({"status": "Template_updated"})
    except  Template.DoesNotExist:
        return JsonResponse({"status": "Template_doesnot_exist"})


    finally:
        print("execution_completed")
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['DELETE'])
def delete_template(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    try:

        template = Template.objects.get(id=request.query_params.get('template_id'))
        if template is not None:
            template.delete()

            return JsonResponse({"status": "Template_deleted"})
    except  Template.DoesNotExist:
        return JsonResponse({"status": "Template_does_not_exist"})


    finally:
        print("execution_completed")
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# TemplateDetails_pagination_Serializer

@api_view(['GET'])
def Templates_pagination(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    if request.method == "GET":
        page = request.query_params.get("page", 1)
        page_size = 10  # Change this to the number of records you want per page

        try:
            page = int(page)
            if page < 1:
                return JsonResponse({"status": "invalid_page_number"}, status=200)
        except ValueError:
            return JsonResponse({"status": "invalid_page_number"}, status=200)

        start_index = (page - 1) * page_size
        end_index = page * page_size

        # Fetch only the records for the current page
        template_list = Template.objects.all().order_by('-id')[start_index:end_index]

        # Check if there are no records for the given page
        if not template_list:
            return JsonResponse({"status": "page_not_found"}, status=200)

        serializer = TemplateDetails_pagination_Serializer(template_list, many=True)

        # Calculate the total number of pages
        total_templates = Template.objects.count()
        total_pages = (total_templates + page_size - 1) // page_size

        response = {
            "number_of_pages": total_pages,
            "current_page": page,
            "next_page": page + 1 if end_index < total_templates else None,
            "previous_page": page - 1 if start_index > 0 else None,
            "templates": serializer.data
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['POST'])
#
def create_broadcast(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    data = request.data
    print("request ............data", data)
    print("type", type(data))

    try:
        template_id=data.get("template_id")
        frequency=data.get("frequency")
        follow_up=data.get("follow_up")
        users=data.get("users")
        category=data.get("category")
        # Fetch the existing broadcasts based on the provided parameters
        # Broadcast_exists = Broadcast.objects.filter(
        #     template=data.get("template_id"),
        #     users__in=data.get("users"),
        #     # users__user_id__username__in=["neerajpynam_hct@gmail.com","neerajpynam3@gmail.com"],
        #     frequency=data.get("frequency"),
        #     follow_up=data.get("follow_up")
        # )
        # print("Broadcast_exists", Broadcast_exists)
        #
        # if Broadcast_exists.exists():
        #     # If there are any existing broadcasts, return a response indicating this
        #     return JsonResponse({"status": "Broadcast_exists"})
        broadcast_users_exist = Broadcast.objects.filter(
            template=template_id,
            frequency=frequency,
            follow_up=follow_up,
            users__in=users
        ).distinct()

        # Query for records based on category
        broadcast_category_exist = Broadcast.objects.filter(
            template=template_id,
            frequency=frequency,
            follow_up=follow_up,
            category=category
        ).distinct()

        # Determine response based on query results
        if broadcast_users_exist.exists() and category is None:
            return JsonResponse({
                "status": "exists",
                "message": "A record exists for the given users list."
                # "record": broadcast_users_exist.first()
            })
        elif broadcast_category_exist.exists() and not users:
            return JsonResponse({
                "status": "exists",
                "message": "A record exists for the given category."
                # "record": broadcast_category_exist.first()
            })
        elif broadcast_users_exist.exists() and broadcast_category_exist.exists():
            return JsonResponse({
                "status": "exists",
                "message": "Records exist for both users list and category."
                # "records": {
                #     "users": broadcast_users_exist.first(),
                #     "category": broadcast_category_exist.first()
                # }
            })

        else:
            print("try else")
            # template_namee = request.data.get('template_name')
            template = Template.objects.get(id=request.data.get('template_id'))
            # print(template.id)
            # category=Category.objects.get(id=request.data.get('category'))
            # # If no existing broadcasts, create a new one
            new_broadcast = Broadcast.objects.create(
                template=template,
                frequency=request.data.get('frequency'),
                follow_up=request.data.get('follow_up'),
                time=request.data.get('time'),
                # category= category
            )
            new_broadcast.users.set(request.data.get('users'))  # Assuming 'users' is a ManyToMany field
            new_broadcast.category.set(request.data.get('categories'))  # Assuming 'users' is a ManyToMany field
            new_broadcast.save()
            return JsonResponse({"status": "Broadcast_added_successfully"})

    except Exception as e:
        # Handle unexpected errors
        print("in except......")
        return JsonResponse({"status": "Error", "message": str(e)})

    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# @api_view(['PUT'])
# #
# def update_broadcast(request):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # if request.user.is_authenticated:
#     data = request.data
#     print("data", data)
#     try:
#         # Fetch the existing broadcasts based on the provided parameters
#         Broadcast_exists = Broadcast.objects.filter(
#             template=data.get("template_id"))
#         print("Broadcast_exists", Broadcast_exists)
#
#         if Broadcast_exists.exists():
#             template = Template.objects.get(id=request.data.get('new_template_id'))
#             # category = Category.objects.get(id=request.data.get('category'))
#             for broadcast in Broadcast_exists:
#                 broadcast.users.set(request.data.get('users'))  # Assuming 'users' is a ManyToMany field
#                 broadcast.template = template
#                 broadcast.frequency = data.get('frequency')
#                 broadcast.follow_up = data.get('follow_up')
#                 broadcast.category.set(request.data.get('categories'))
#                 broadcast.time = data.get('time')
#             #
#             broadcast.save()
#
#             # If there are any existing broadcasts, return a response indicating this
#             return JsonResponse({"status": "Broadcast_updated"})
#         else:
#
#             return JsonResponse({"status": "No_Broadcast_exists"})
#
#     except Exception as e:
#         # Handle unexpected errors
#         return JsonResponse({"status": "Error", "message": str(e)})
#     # else:
#     #     return JsonResponse({"status": "unauthorized_user"})
@api_view(['PUT'])
def update_broadcast(request):
    data = request.data
    print("data", data)
    try:
        # Fetch the existing broadcasts based on the provided parameters
        Broadcast_exists = Broadcast.objects.filter(id=data.get("broadcast_id"),template=data.get("template_id"))
        print("Broadcast_exists", Broadcast_exists)

        if Broadcast_exists.exists():
            template = Template.objects.get(id=request.data.get('new_template_id'))

            # Iterate through the broadcasts and update them
            for broadcast in Broadcast_exists:
                users = request.data.get('users', [])
                categories = request.data.get('categories', [])

                if users:
                    broadcast.users.set(users)  # Assuming 'users' is a ManyToMany field

                broadcast.template = template
                broadcast.frequency = data.get('frequency', broadcast.frequency)
                broadcast.follow_up = data.get('follow_up', broadcast.follow_up)

                if categories:
                    broadcast.category.set(categories)  # Assuming 'categories' is a ManyToMany field

                if 'time' in data:
                    broadcast.time = data.get('time', broadcast.time)

                broadcast.save()
                print('broadcast',broadcast.category)

            return JsonResponse({"status": "Broadcast_updated"})
        else:
            return JsonResponse({"status": "No_Broadcast_exists"})

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"status": "Error", "message": str(e)})


@api_view(['DELETE'])
def delete_broadcast(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    try:

        broadcast = Broadcast.objects.get(id=request.query_params.get('broadcast_id'))
        print(broadcast)
        if broadcast is not None:
            broadcast.delete()

            return JsonResponse({"status": "Broadcast_deleted"})
    except  broadcast.DoesNotExist:
        return JsonResponse({"status": "Broadcast_does_not_exist"})


    finally:
        print("execution_completed")
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


# hct_template_dd

@api_view(['GET'])
def hct_template_dd(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    active_users_list = []
    if request.method == 'GET':
        template_names = Template.objects.all().values("template_name", "id")
        print('template_names', template_names, type(template_names))
        template_serializer = Template_dropdown_Serializer(template_names, many=True)
        print(template_serializer)
        template_serializer_data = template_serializer.data
        print(template_serializer_data)

        template_list = [{'template_id': template['id'], 'template_name': template['template_name']} for template in
                         template_serializer_data]

        return JsonResponse({"template_list": template_list})
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['GET'])
def broadcast_pagination(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    if request.method == "GET":
        page = request.query_params.get("page", 1)
        page_size = 10  # Change this to the number of records you want per page

        try:
            page = int(page)
            if page < 1:
                return JsonResponse({"status": "invalid_page_number"}, status=200)
        except ValueError:
            return JsonResponse({"status": "invalid_page_number"}, status=200)

        start_index = (page - 1) * page_size
        end_index = page * page_size

        # Fetch only the records for the current page
        broadcast_list = Broadcast.objects.all().order_by('-id')[start_index:end_index]
        print('broadcast_list',broadcast_list)

        # Check if there are no records for the given page
        if not broadcast_list:
            return JsonResponse({"status": "page_not_found"}, status=200)

        serializer = Broadcast_Serializer(broadcast_list, many=True)
        # print(serializer)
        # print(serializer.data)
        # Calculate the total number of pages
        total_broadcasts = Broadcast.objects.count()
        total_pages = (total_broadcasts + page_size - 1) // page_size

        response = {
            "number_of_pages": total_pages,
            "current_page": page,
            "next_page": page + 1 if end_index < total_broadcasts else None,
            "previous_page": page - 1 if start_index > 0 else None,
            "templates": serializer.data
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})






@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        # Extract username and business_email from the request data
        username = request.data.get('username')
        business_email = request.data.get('business_email')

        # Check if username or business_email is missing
        if not username or not business_email:
            return JsonResponse(
                {"status": "failed", "error": "Both username and business_email are required."},
                status=200
            )

        # Check if a user with this username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": "failed", "error": f"Username '{username}' is already taken."},
                status=200
            )

        # Check if a user with this business_email already exists in User_details
        if User_details.objects.filter(business_email=business_email).exists():
            return JsonResponse(
                {"status": "failed", "error": f"Email '{business_email}' is already registered."},
                status=200
            )

        # If both username and business_email are unique, proceed with serialization and creation
        serializer = User_create_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "user_registered_successfully"}, status=201)
        else:
            return JsonResponse({"status": "failed", "errors": serializer.errors}, status=200)

    # Handle non-POST requests (optional)
    return JsonResponse({"status": "failed", "error": "Only POST requests are allowed."}, status=200)




@api_view(['GET'])
def hct_category_dd(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:
    active_users_list = []
    if request.method == 'GET':
        categories = Category.objects.all()
        print('categories', categories, type(categories))
        categories_serializer = category_Serializer(categories, many=True)
        print(categories_serializer)
        categories_serializer_data = categories_serializer.data
        print('//////////////', categories_serializer_data)

        categories_list = [{'category_id': category['id'], 'category': category['category']} for category in
                             categories_serializer_data]

        return JsonResponse({"category_list": categories_list})




@api_view(['POST'])
def send_message_template(request):
    print("enter")
    try:

        url = "https://graph.facebook.com/v21.0/422738437582013/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": "916304882347",
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
            'Authorization': 'Bearer EAAMY4TVLDQ4BOyx2L1jGZB7AQWkTes3FHMYHwAjTIkP6LC0RGmaLuhVbyS15xBQ0Hf3Ve564kB0PFe8ZA5ly007AW7eeipXhTKKl1gbUZAfzsx2Wi99Hyg6TfErSafHOv0bMEhK4lcGp0QRj9tdJGbfoNtLUhTCG6kOAnr0XMbSUnb4gOEWJfb4Fx9DiqrgLXWjbZBEyimMO7pUg2UxBH6rBMxwZD'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        if response.status_code == 200:
            # Parse JSON response
            response_data = response.json()
            return JsonResponse(response_data)
        else:
            # If the request was not successful, return an error message
            return JsonResponse({'error': 'Failed to send data to external API'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error exception': e})



# class BulkUserUploadView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         file = request.FILES.get('file')  #  Captures the uploaded file
#         if not file:
#             return JsonResponse({"error": "No file uploaded"}, status=400)
#
#         try:
#             wb = openpyxl.load_workbook(file)  #  Reads the file using openpyxl
#             sheet = wb.active  #  Gets the first sheet
#
#             users_created = []
#             errors = []
#
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 username, name, contact_no, business_email, location, age, gender, category_name, user_status = row
#
#                 if not all([username, name, contact_no, business_email, location, age, gender, category_name, user_status]):
#                     errors.append({"row": row, "error": "Missing required fields"})
#                     continue
#
#                 try:
#                     category = Category.objects.get(category=category_name)
#                 except Category.DoesNotExist:
#                     errors.append({"row": row, "error": f"Category '{category_name}' not found"})
#                     continue
#
#                 user_data = {
#                     "username": username,
#                     "name": name,
#                     "contact_no": contact_no,
#                     "business_email": business_email,
#                     "location": location,
#                     "age": age,
#                     "gender": gender,
#                     "category": category.id,
#                     "user_status": user_status
#                 }
#
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


#https://hct.automactechnologies.in/
@api_view(['GET'])
def challenge_pagination(request):
    if request.method == "GET":
        page = request.query_params.get("page", 1)
        page_size = 10  # Change this to the number of records you want per page
        param_category = request.query_params.get("category")

        try:
            page = int(page)
            if page < 1:
                return JsonResponse({"status": "invalid_page_number"}, status=200)
        except ValueError:
            return JsonResponse({"status": "invalid_page_number"}, status=200)

        start_index = (page - 1) * page_size
        end_index = page * page_size

        # Fetch only the records for the current page
        broadcast_list = User_details.objects.filter(user_status="active", category__category=param_category).order_by('-id')[start_index:end_index]

        # Check if there are no records for the given page
        if not broadcast_list:
            return JsonResponse({"status": "page_not_found"}, status=200)

        serializer = challange_Serializer(broadcast_list, many=True)

        # Calculate the total number of pages
        total_broadcasts = User_details.objects.filter(user_status="active", category__category=param_category).count()
        total_pages = (total_broadcasts + page_size - 1) // page_size

        response = {
            "number_of_pages": total_pages,
            "current_page": page,
            "next_page": page + 1 if end_index < total_broadcasts else None,
            "previous_page": page - 1 if start_index > 0 else None,
            "challenge_records": serializer.data,
            "no_of_records": len(serializer.data)
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)
#
# @api_view(['PATCH'])
# def user_onboard(request):
#     if request.method == 'PATCH':
#         # Extract user_id from request data
#         user_id = request.data.get('user_id')
#
#         # Validate user_id presence
#         if not user_id:
#             return JsonResponse({"error": "user_id_is_required"}, status=400)
#
#         try:
#             # Fetch the existing User_details instance
#             user_details = User_details.objects.get(user_id=user_id)
#             print('user_details',user_details)
#         except User_details.DoesNotExist:
#             return JsonResponse({"error": "User_details_not_found"}, status=404)
#         except User_details.MultipleObjectsReturned:
#             return JsonResponse({"error": "Multiple_user_details_found_for_this_user_id"}, status=400)
#
#         # Use serializer for partial update
#         serializer = User_onboard_CreateSerializer(user_details, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({"status": "user_onboarded_successfully"}, status=200)
#         else:
#             return JsonResponse({"error": serializer.errors}, status=400)
#     return JsonResponse({"error": "Method_not_allowed"}, status=405)

@api_view(['DELETE'])
def delete_onboard_user(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    try:

        all_rec = User_tracking.objects.filter(user_id=request.query_params.get('user_id'))
        if all_rec.exists():
            all_rec.delete()
            return JsonResponse({"status": "user_records_deleted"})
        else:
            return JsonResponse({"status": "No_records_found"})
    except  all_rec.DoesNotExist:
        return JsonResponse({"status": "records_does_not_exist"})


    finally:
        print("execution_completed")
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['GET'])
def user_challenge_records_pagination(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    if request.method == "GET":
        page = request.query_params.get("page", 1)
        page_size = 10  # Change this to the number of records you want per page

        try:
            page = int(page)
            if page < 1:
                return JsonResponse({"status": "invalid_page_number"}, status=200)
        except ValueError:
            return JsonResponse({"status": "invalid_page_number"}, status=200)

        start_index = (page - 1) * page_size
        end_index = page * page_size

        # Fetch only the records for the current page
        broadcast_list = User_tracking.objects.filter(user_id=request.query_params.get("user_id")).order_by('-id')[start_index:end_index]
        print('broadcast_list',broadcast_list)

        # Check if there are no records for the given page
        if not broadcast_list:
            return JsonResponse({"status": "page_not_found"}, status=200)

        serializer = UserTrackingSerializer(broadcast_list, many=True)
        # print(serializer)
        # print(serializer.data)
        # Calculate the total number of pages
        # total_broadcasts = User_tracking.objects.count()
        total_broadcasts = User_tracking.objects.filter(user_id=request.query_params.get("user_id")).count()
        total_pages = (total_broadcasts + page_size - 1) // page_size

        response = {
            "number_of_pages": total_pages,
            "current_page": page,
            "next_page": page + 1 if end_index < total_broadcasts else None,
            "previous_page": page - 1 if start_index > 0 else None,
            "user_daily_activity_records": serializer.data
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['POST'])
def user_challenge_create_records(request):
    try:
        # Extract user_id and date_of_activity from request data
        user_id = request.data.get('user_id')
        date_of_activity = request.data.get('date_of_activity')

        # Validate user_id and date_of_activity
        if not user_id or not date_of_activity:
            return Response(
                {"status": "user_id_and_date_of_activity_required"},
                status=status.HTTP_200_OK
            )

        # Convert user_id to User instance if necessary (assuming user_id is an ID)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "user_not_found"},
                status=status.HTTP_200_OK
            )

        # Parse date_of_activity to ensure it's in the correct format
        try:
            parsed_date = datetime.strptime(date_of_activity, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"status": "invalid_date_format_use_YYYY-MM-DD"},
                status=status.HTTP_200_OK
            )

        # Check if a record exists for the given user_id and date_of_activity
        existing_record = User_tracking.objects.filter(
            user_id=user,
            date_of_activity=parsed_date
        ).exists()

        if existing_record:
            return Response(
                {"status": "record_already_exists_for_this_user_and_date"},
                status=status.HTTP_200_OK
            )

        # Use serializer for validation and creation
        serializer = UserTrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"status": "user_tracking_created"},
                status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse(
                {"status": "invalid_data", "errors": serializer.errors},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return JsonResponse(
            {"status": f"error: {str(e)}"},
            status=status.HTTP_200_OK
        )



@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def userr_challenge_create_records(request):
    try:
        # Extract user_id and date_of_activity from request data
        user_id = request.data.get('user_id')
        date_of_activity = request.data.get('date_of_activity')

        # Validate user_id and date_of_activity
        if not user_id or not date_of_activity:
            return Response(
                {"status": "user_id_and_date_of_activity_required"},
                status=status.HTTP_200_OK
            )

        # Convert user_id to User instance if necessary (assuming user_id is an ID)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "user_not_found"},
                status=status.HTTP_200_OK
            )

        # Parse date_of_activity to ensure it's in the correct format
        try:
            parsed_date = datetime.strptime(date_of_activity, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"status": "invalid_date_format_use_YYYY-MM-DD"},
                status=status.HTTP_200_OK
            )

        # Check if a record exists for the given user_id and date_of_activity
        existing_record = User_tracking.objects.filter(
            user_id=user,
            date_of_activity=parsed_date
        ).exists()

        if existing_record:
            return Response(
                {"status": "record_already_exists_for_this_user_and_date"},
                status=status.HTTP_200_OK
            )

        # Use serializer for validation and creation
        serializer = UserTrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"status": "user_tracking_created"},
                status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse(
                {"status": "invalid_data", "errors": serializer.errors},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return JsonResponse(
            {"status": f"error: {str(e)}"},
            status=status.HTTP_200_OK
        )


@api_view(['PUT'])
def update_user_tracking(request):
    try:
        # Extract user_id, date_of_activity, and new_date_of_activity
        user_id = request.data.get('user_id')
        date_of_activity = request.data.get('date_of_activity')
        new_date_of_activity = request.data.get('new_date_of_activity')

        # Check if user_id and date_of_activity are provided for fetching record
        if not (user_id and date_of_activity):
            return JsonResponse(
                {"status": "user_id_and_date_of_activity_are_required"},
                status=status.HTTP_200_OK
            )

        # Fetch the existing record
        user_tracking = User_tracking.objects.filter(
            user_id=user_id,
            date_of_activity=date_of_activity
        ).first()

        if not user_tracking:
            return JsonResponse(
                {"status": "Record_does_not_exist"},
                status=status.HTTP_200_OK
            )

        # Prepare data for update, including new_date_of_activity if provided
        update_data = request.data.copy()
        if new_date_of_activity:
            update_data['date_of_activity'] = new_date_of_activity

        # Use serializer to update the record
        serializer = UserTrackingSerializer(user_tracking, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"status": "User_tracking_updated"},
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"status": "Invalid_data", "errors": serializer.errors},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return JsonResponse({"status": str(e)}, status=status.HTTP_200_OK)




@api_view(['DELETE'])
def delete_user_activity_record(request):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # if request.user.is_authenticated:

    try:

        usr_activity_record = User_tracking.objects.get(user_id=request.query_params.get('user_id'),date_of_activity=request.query_params.get('date_of_activity'))
        if usr_activity_record is not None:
            usr_activity_record.delete()

            return JsonResponse({"status": "user_activity_record_deleted"})
    except  usr_activity_record.DoesNotExist:
        return JsonResponse({"status": "user_activity_record_does_not_exist"})


    finally:
        print("execution_completed")
    # else:
    #     return JsonResponse({"status": "unauthorized_user"})


@api_view(['GET'])
def user_challenge_records_all(request):
    if request.method == "GET":
        # Fetch all records for the specified user
        user_id = request.query_params.get("user_id")
        if not user_id:
            return JsonResponse({"status": "missing_user_id"}, status=400)

        broadcast_list = User_tracking.objects.filter(user_id=user_id).order_by('-id')

        # Check if there are any records
        if not broadcast_list:
            return JsonResponse({"status": "no_records_found"}, status=200)

        serializer = UserTrackingSerializer(broadcast_list, many=True)

        response = {
            "total_records": broadcast_list.count(),
            "user_daily_activity_records": serializer.data
        }

        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"status": "method_not_allowed"}, status=405)


@api_view(['POST'])
def category_create(request):
    # Validate category field
    category = request.data.get('category', '').strip()
    if not category:
        return JsonResponse(
            {
                "status": "Category_name_cannot_be_empty."

            }
        )

    # Check for duplicate category (case-insensitive)
    if Category.objects.filter(category__iexact=category).exists():
        return JsonResponse(
            {
                "status": "Category_already_exists."

            }
        )

    # Serialize and save
    serializer = category_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(
            {
                "status": "Category_created_successfully",

            }
        )

    # Handle any other serializer errors
    return JsonResponse(
        {
            "status": "Failed_to_create_category",
            "errors": serializer.errors
        }
    )
