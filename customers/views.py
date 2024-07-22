from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def cprofile(request):
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            user = user_form.save(commit=False)
            user.save()

            messages.success(request, 'Profile Updated Successfully')
            return redirect('cprofile')
        else:
            messages.error(request, 'Error updating profile.')
            print(f"Profile form error is {profile_form.errors}")
            print(f"User form error is {user_form.errors}")
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }

    return render(request, 'customers/cprofile.html', context)