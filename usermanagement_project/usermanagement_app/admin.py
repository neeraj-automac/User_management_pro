from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class SampleAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UserDetailsInline(admin.StackedInline):
    model = User_details
    can_delete = False

class UserDetailsAdmin(AuthUserAdmin):
    list_display =['id','username']
    def add_view(self,*args,**kwargs):#for error
        self.inlines=[]
        return super(UserDetailsAdmin, self).add_view(*args, **kwargs)

    def change_view(self,*args,**kwargs):
        self.inlines =[UserDetailsInline]
        return super(UserDetailsAdmin, self).change_view(*args, **kwargs)


    #inlines=[UserProfileInline]






admin.site.unregister(User)
admin.site.register(User,UserDetailsAdmin)







@admin.register(User_details)
class User_detailsAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','user_status','name','category','Total_workout_duration','formatted_duration']

    def formatted_duration(self, obj):
        return obj.get_formatted_duration()

    formatted_duration.short_description = 'Workout Duration'
# @admin.register(User_registration)
# class User_registrationAdmin(admin.ModelAdmin):
#     list_display = ["name","category","email","gender"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category']











@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name','template_heading']


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    # list_display = ['id','template','users','category','frequency','follow_up','sent_status']
    list_display = ['id','template','frequency','follow_up','sent_status']

@admin.register(User_tracking)
class User_trackingAdmin(admin.ModelAdmin):
    # list_display = ['id','template','users','category','frequency','follow_up','sent_status']
    list_display = ['user_id','category','date_of_activity','day_count','step_count','workout_duration']



# User_tracking
# @admin.register(User_tracking)
# class User_trackingAdmin(admin.ModelAdmin):
#     list_display = ['user_id', 'category', 'date_of_activity', 'day_count', 'step_count', 'formatted_workout_duration']
#
#     def formatted_workout_duration(self, obj):
#         duration = obj.workout_duration
#         if duration:
#             total_seconds = int(duration.total_seconds())
#             hours = total_seconds // 3600
#             minutes = (total_seconds % 3600) // 60
#             return f"{hours}h {minutes}m"
#         return "-"
#     formatted_workout_duration.short_description = 'Workout Duration'


# @admin.register(User_details)
# class User_detailsAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_id', 'user_status', 'name', 'category', 'formatted_total_workout_duration']
#
#     def formatted_total_workout_duration(self, obj):
#         duration = obj.Total_workout_duration
#         if duration:
#             total_seconds = int(duration.total_seconds())
#             hours = total_seconds // 3600
#             minutes = (total_seconds % 3600) // 60
#             return f"{hours}h {minutes}m"
#         return "-"
#     formatted_total_workout_duration.short_description = 'Total Workout Duration'




