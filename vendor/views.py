from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import VendorForm
from menu.forms import categoryForm, FoodItemForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from django.template.defaultfilters import slugify


#Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)

@login_required
def vprofile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        vendor = Vendor.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')  # Redirect to an appropriate page

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }

    return render(request, 'vendor/menu_builder.html', context)

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

def fooditems_by_category(request, pk=None):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None

    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    print(fooditems)
    context = {
        'fooditems': fooditems,
        'category': category,
    }

    return render(request, 'vendor/fooditems_by_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = categoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            category_exist = Category.objects.filter(slug=slug).exists()
            if category_exist:
                form.add_error('category_name', 'A category with this name already exists.')
            else:
                category = form.save(commit=False)
                category.vendor = get_vendor(request)
                category.slug = slug
                form.save()
                messages.success(request, 'category added successfully!')
                return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = categoryForm()
        # modify form
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
         'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = categoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            slug = slugify(category_name)
            category.slug = slug
            form.save()
            messages.success(request, 'category Updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = categoryForm(instance=category)
    context = {
         'form': form,
        'category': category,
    }

    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category Deleted Successfully")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            slug = slugify(food_title)
            food_exist = Category.objects.filter(slug=slug).exists()
            if food_exist:
                form.add_error('food_title', 'A Food Item with this name already exists.')
            else:
                food = form.save(commit=False)
                food.vendor = get_vendor(request)
                food.slug = slug
                form.save()
                messages.success(request, 'Food Item added successfully!')
                return redirect('fooditems_by_category', food.category.id)
        else:
            messages.error(request, 'Failed to add Food Item! Check your form')
            print(form.errors)

    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
         'form': form,
    }
    return render(request, 'vendor/add_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            slug = slugify(food_title)
            food.slug = slug
            form.save()
            messages.success(request, 'Food Item Updated successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
         'form': form,
         'food': food,
    }

    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, "Food Item Deleted Successfully")
    return redirect('fooditems_by_category', food.category.id)
