from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:9]
    print(f"vendors = {vendors}")
    context = {
        'vendors': vendors,
    }
    return render(request, "index.html", context)
