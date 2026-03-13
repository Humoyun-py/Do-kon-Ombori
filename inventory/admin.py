"""
Django admin configuration for inventory app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Role, UserProfile, Category, Supplier, Product, Stock, 
    Transaction, TelegramUser, Notification, Report
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone_number', 'city', 'is_active']
    list_filter = ['is_active', 'city', 'created_at']
    search_fields = ['name', 'contact_person', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'quantity', 'stock_status', 'price', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'code', 'category', 'supplier', 'description')
        }),
        ('Narx va miqdor', {
            'fields': ('price', 'quantity', 'unit', 'min_stock')
        }),
        ('Qo\'shimcha', {
            'fields': ('image', 'is_active', 'created_at', 'updated_at')
        }),
    )
    
    def stock_status(self, obj):
        status = obj.get_status()
        if status == 'out_of_stock':
            color = 'red'
            text = 'Tugagan'
        elif status == 'low_stock':
            color = 'orange'
            text = 'Kam'
        else:
            color = 'green'
            text = 'Yetarli'
        return format_html(
            '<span style="color: {};">{}</span>',
            color, text
        )
    stock_status.short_description = 'Status'


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'last_updated', 'updated_by']
    list_filter = ['last_updated']
    search_fields = ['product__name', 'product__code']
    readonly_fields = ['last_updated']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'reference_number', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'created_at', 'product__category']
    search_fields = ['product__name', 'product__code', 'reference_number']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'username', 'user', 'is_active', 'notifications_enabled']
    list_filter = ['is_active', 'notifications_enabled', 'created_at']
    search_fields = ['telegram_id', 'username', 'first_name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'read_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'start_date', 'end_date', 'generated_by', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at']
