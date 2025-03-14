
from django.db import models
from django.utils.text import slugify
from django.db import models
# from django.contrib.auth.models import User
from accounts.models import User, UserProfile
from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

# class Vendor(models.Model):
#     user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
#     user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
#     vendor_name = models.CharField(max_length=50)
#     vendor_slug = models.SlugField(max_length=100, blank=True)
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now_add=True)
#     # Other fields and methods for the Vendor model

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if not self.vendor_slug and self.vendor_name:
            self.vendor_slug = slugify(self.vendor_name)
        #checking if a vendor is approved fot it to display its menu
        if self.pk is not None:
            mail_template = 'accounts/emails/admin_approval_email.html'
            context = {
                'user': self.user,
                'is_approved': self.is_approved,
                'to_email': self.user.email,
            }
            # update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                if self.is_approved == True:

                    # send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved"

                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "We are sorry! You are not eligible for publishing your food menu on our marketplace"
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
