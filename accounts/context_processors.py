from vendor.models import Vendor
from .models import UserProfile
from foodonline import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        # profile = {
        #     'profile_picture': user_profile.profile_picture,
        #     'cover_photo': user_profile.cover_photo,
        # }
    except:
        user_profile = None
    return dict(profile=user_profile)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None

    return dict(user_profile=user_profile)

def get_paypal_client_id(request):
    return {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID
    }

