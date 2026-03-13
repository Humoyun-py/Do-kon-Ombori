"""
Data models for warehouse inventory management system.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime


class Role(models.Model):
    """User roles: Admin, Warehouseman, Shop Staff"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('warehouseman', 'Omborchi'),
        ('staff', 'Do\'kon xodimi'),
    ]
    
    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class UserProfile(models.Model):
    """Extended user profile with role and warehouse info"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def get_role_display(self):
        if self.role:
            return self.role.get_name_display()
        return "No Role"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Supplier(models.Model):
    """Product suppliers"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']


class Product(models.Model):
    """Product information"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    unit = models.CharField(max_length=20, default='dona')  # dona, kg, litr, etc.
    min_stock = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def is_low_stock(self):
        return self.quantity < self.min_stock
    
    def get_status(self):
        if self.quantity == 0:
            return 'out_of_stock'
        elif self.is_low_stock():
            return 'low_stock'
        return 'in_stock'
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category']),
        ]


class Stock(models.Model):
    """Warehouse stock tracking"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'


class Transaction(models.Model):
    """Transaction history for product movements"""
    TRANSACTION_TYPE = [
        ('income', 'Kirim'),
        ('outcome', 'Chiqim'),
        ('adjustment', 'Sozlash'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.code} - {self.get_transaction_type_display()} ({self.quantity})"
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
        ]


class TelegramUser(models.Model):
    """Telegram users connected to the system"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='telegram_user')
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    notifications_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} (@{self.username}) - {self.telegram_id}"
    
    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'


class Notification(models.Model):
    """System notifications"""
    NOTIFICATION_TYPE = [
        ('low_stock', 'Kam qolgan mahsulot'),
        ('new_income', 'Yangi kirim'),
        ('system_alert', 'Tizim ogohlantirishi'),
        ('user_message', 'Foydalanuvchi xabari'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE)
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']


class Report(models.Model):
    """Reports and analytics storage"""
    REPORT_TYPE = [
        ('summary', 'Umumiy'),
        ('income', 'Kirim'),
        ('outcome', 'Chiqim'),
        ('stock', 'Qoldiq'),
        ('product_movement', 'Mahsulot harakati'),
        ('supplier', 'Yetkazib beruvchi'),
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    data = models.JSONField(default=dict, blank=True)
    
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
