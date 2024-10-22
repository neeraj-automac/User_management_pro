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
    list_display = ['id','name']

@admin.register(User_registration)
class User_registrationAdmin(admin.ModelAdmin):
    list_display = ["name","category","email","gender"]













@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name','template_heading']


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['template','frequency','follow_up','sent_status']






