"""
Authentication views for login, registration and password reset
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse_lazy
from .models import UserProfile, Role


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Set session expiry if "Remember me" not checked
            if not remember:
                request.session.set_expiry(0)
            
            # Redirect to next page or dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri!')
    
    context = {}
    return render(request, 'login.html', context)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validation
        errors = {}
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Bu foydalanuvchi nomi allaqachon olingan'
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Bu email manzil allaqachon ro\'yxatdan o\'tgan'
        
        # Check password length
        if len(password1) < 8:
            errors['password1'] = 'Parol kamida 8 ta belgidan iborat bo\'lishi kerak'
        
        # Check if passwords match
        if password1 != password2:
            errors['password2'] = 'Parollar mos kelmadi'
        
        # Check if password has letters and numbers
        if not any(char.isalpha() for char in password1) or not any(char.isdigit() for char in password1):
            errors['password1'] = 'Parolda harf va raqamlar bo\'lishi kerak'
        
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create default role (shop staff)
            staff_role = Role.objects.get_or_create(name='staff')[0]
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role=staff_role
            )
            
            messages.success(request, '✅ Ro\'yxatdan muvaffaqiyatli o\'tdingiz! Endi kirishalas:')
            return redirect('login')
    
    context = {}
    return render(request, 'register.html', context)


@login_required
def logout_view(request):
    """User logout view"""
    auth_logout(request)
    messages.success(request, '👋 Tizimdan chiqib qoldiniz')
    return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view"""
    template_name = 'password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        messages.info(self, 'Parol tiklash uchun email yuborildi. Email-ni tekshiring.')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view"""
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self, 'Parol muvaffaqiyatli o\'zgartirildi!')
        return super().form_valid(form)


def password_reset_done_view(request):
    """Password reset done view"""
    return render(request, 'password_reset_done.html')


def password_reset_complete_view(request):
    """Password reset complete view"""
    return render(request, 'password_reset_done.html')
