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
    path('broadcast_pagination/',views.Broadcast_pagination,name='Broadcast_pagination'),


]