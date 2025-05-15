from django.urls import path
from . import views
from .views import*


urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('all_users_status/',views.all_users_status),
    path('delete_users/',views.delete_users),
    path('update_user_status/',views.update_user_status),
    path('pagination/',views.pagination),
    path('edit_user_details_hct/',views.edit_user_details_hct),
    path('broadcast/', views.broadcast, name='broadcast'),
    path('hct_active_users_dd/', views.hct_active_users, name='hct_active_users'),
    path('create_template/', views.create_template, name='create_template'),
    path('update_template/', views.update_template, name='update_template'),
    path('delete_template/', views.delete_template, name='delete_template'),
    path('template_pagination/',views.Templates_pagination,name='Templates_pagination'),
    path('create_broadcast/', views.create_broadcast, name='create_broadcast'),
    path('update_broadcast/', views.update_broadcast, name='update_broadcast'),
    path('delete_broadcast/', views.delete_broadcast, name='delete_broadcast'),
    path('hct_template_dd/', views.hct_template_dd, name='hct_template_dd'),
    path('hct_category_dd/', views.hct_category_dd, name='hct_template_dd'),
    path('broadcast_pagination/',views.broadcast_pagination,name='broadcast_pagination'),
    path('send_message_template/',views.send_message_template,name='send_message_template'),
    path('challenge_pagination/',views.challenge_pagination,name='challenge_pagination'),
    # path('user_onboard/', views.user_onboard, name='user_onboard'),
    path('delete_onboard_user/', views.delete_onboard_user, name='user_onboard'),
    path('user_challenge_records/', views.user_challenge_records_pagination, name='user_challenge_records_pagination'),
    path('user_challenge_create_records/', views.user_challenge_create_records, name='user_challenge_create_records'),
    path('userr_challenge_create_records/', views.userr_challenge_create_records, name='userr_challenge_create_records'),
    path('update_user_tracking/', views.update_user_tracking, name='update_user_tracking'),
    path('delete_user_activity_record/', views.delete_user_activity_record, name='delete_user_activity_record'),
    path('user_challenge_records_all/', views.user_challenge_records_all, name='user_challenge_records_all'),
    path('category_create/', category_create, name='category_create-create')
    # path('upload-users/', BulkUserUploadView.as_view(), name='upload-users'),


]