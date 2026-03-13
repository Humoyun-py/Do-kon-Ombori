"""
URL configuration for inventory app
"""

from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from . import views
from . import auth_views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('password-reset/', auth_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.password_reset_complete_view, name='password_reset_complete'),
    
    # Main app URLs
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:product_id>/transaction/', views.add_transaction, name='add_transaction'),
    path('reports/stock/', views.stock_report, name='stock_report'),
    path('reports/transactions/', views.transaction_report, name='transaction_report'),
]
