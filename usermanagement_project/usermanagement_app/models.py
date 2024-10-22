from datetime import timedelta
from datetime import time
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.fields import EmailField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Min, Max
from django.core.mail import send_mail
from django.conf import settings

class User_details(models.Model):
    objects = models.Manager()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE )
    ROLE_STATUS_CHOICES = (('admin', 'admin'), ('customer', 'customer'))
    role = models.CharField(max_length=15, choices=ROLE_STATUS_CHOICES)
    name=models.CharField(max_length = 50,blank=False)
    contact_no = models.BigIntegerField()
    user_status=models.CharField(max_length = 50,blank=True)
    company = models.CharField(max_length = 30,blank=True)#remove?
    business_email = models.EmailField(max_length = 254,blank=False)
    years_of_experience = models.PositiveSmallIntegerField(null=True, blank=True)#remove?
    job_position = models.CharField(max_length = 30,blank=True)#remove?
    location = models.CharField(max_length = 30,blank=False)
    otp = models.CharField(max_length=255, unique=True, blank=True, null=True)
    course_id=models.IntegerField(null=True, blank=True)




    def __str__(self):
        return self.user_id.username


class User_registration(models.Model):

   name = models.CharField(max_length=100)
   category = models.CharField(max_length=100)
   mobile_num = models.BigIntegerField()
   email = models.EmailField(unique=True)
   location = models.CharField(max_length=100)
   age = models.PositiveIntegerField()
   gender = models.CharField(max_length=150)


   def __str__(self):
       return self.name

















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
    users=models.ManyToManyField(User_details)
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


            print("broadcast_usersssss", instance.users.all())
            email_addresses = list(instance.users.values_list('business_email', flat=True))
            print("User email addresses:", email_addresses, type(email_addresses))
            contact_numbers = list(instance.users.values_list('contact_no', flat=True))
            print("User contact_numbers:", contact_numbers, type(contact_numbers))
            print(instance.template.template_name)
            print(instance.template.template_heading)
            print(instance.template.template_body)
            # email_body = f'''<p>instance.template.template_heading</p>'''
            if instance.frequency == "once" and instance.follow_up == "mail":
                print("sending once via mail")
                send_mail(instance.template.template_heading, '', from_email=settings.EMAIL_HOST_USER,
                          recipient_list=email_addresses, html_message=instance.template.template_body)
                print("sended")

            elif instance.frequency == "periodically" and instance.follow_up == "mail":
                print("sending periodically via mail by calling celery")


            elif instance.frequency == "once" and instance.follow_up == "whatsapp":
                print("sending once via  whastapp")
            elif instance.frequency == "periodic" and instance.follow_up == "whatsapp":
                print("sending periodically via  whatsapp ")

            elif instance.frequency == "once" and instance.follow_up == "both":
                print("sending once via both by calling send mail and whastapp")
            elif instance.frequency == "periodic" and instance.follow_up == "both":
                print("sending periodically via both by calling celery and writting send mail")


            else:
                print("not once not periodic ")

        else:
            print("executing -sent status is False")
    # else:
    #     print("not created not updated")





@receiver(post_save, sender=User_registration)
def send_broadcast(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.name, password="user@123")
        # print(user.is_staff)
        user.save()
        user_details = User_details.objects.create(user_id=user,role="customer",name=instance.name,contact_no=instance.mobile_num,user_status="",company="",business_email=instance.email,years_of_experience=None,job_position="",location=instance.location,otp=None,course_id=None)
        user_details.save()
        print('user_created')
        print("created in user_reg")



    else:

        print("edited in user reg models.py")