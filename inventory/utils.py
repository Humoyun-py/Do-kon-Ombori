"""
Utility functions for warehouse management system
"""

from django.db.models import Q, Sum, F, Count
from inventory.models import Product, Transaction, Notification
from datetime import datetime, timedelta
import json


def get_low_stock_products():
    """Get all low stock products"""
    return Product.objects.filter(
        is_active=True,
        quantity__lt=F('min_stock')
    )


def get_out_of_stock_products():
    """Get all out of stock products"""
    return Product.objects.filter(is_active=True, quantity=0)


def create_notification(title, message, notification_type, product=None, user=None, telegram_user=None):
    """Create a notification"""
    notification = Notification.objects.create(
        title=title,
        message=message,
        notification_type=notification_type,
        product=product,
        user=user,
        telegram_user=telegram_user
    )
    return notification


def get_stock_value():
    """Calculate total warehouse stock value"""
    return Product.objects.filter(is_active=True).aggregate(
        total_value=Sum(F('price') * F('quantity'))
    )['total_value'] or 0


def get_transaction_summary(days=30):
    """Get transaction summary for last N days"""
    start_date = datetime.now() - timedelta(days=days)
    
    income_transactions = Transaction.objects.filter(
        transaction_type='income',
        created_at__gte=start_date
    ).aggregate(
        total_items=Sum('quantity'),
        count=Count('id')
    )
    
    outcome_transactions = Transaction.objects.filter(
        transaction_type='outcome',
        created_at__gte=start_date
    ).aggregate(
        total_items=Sum('quantity'),
        count=Count('id')
    )
    
    return {
        'income': income_transactions,
        'outcome': outcome_transactions,
        'period_days': days
    }


def generate_stock_report():
    """Generate comprehensive stock report"""
    products = Product.objects.filter(is_active=True)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_products': products.count(),
        'low_stock_count': get_low_stock_products().count(),
        'out_of_stock_count': get_out_of_stock_products().count(),
        'total_stock_value': get_stock_value(),
        'products': []
    }
    
    for product in products:
        report['products'].append({
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'quantity': product.quantity,
            'min_stock': product.min_stock,
            'price': float(product.price),
            'status': product.get_status()
        })
    
    return report


def check_and_notify_low_stock():
    """Check for low stock products and create notifications"""
    low_stock_products = get_low_stock_products()
    
    for product in low_stock_products:
        # Check if notification already exists for today
        today = datetime.now().date()
        existing = Notification.objects.filter(
            product=product,
            notification_type='low_stock',
            created_at__date=today
        ).exists()
        
        if not existing:
            create_notification(
                title=f"Kam qolgan: {product.name}",
                message=f"{product.name} mahsulotning qoldig'i {product.quantity} ga tushdi. Minimal: {product.min_stock}",
                notification_type='low_stock',
                product=product
            )


def get_category_statistics():
    """Get statistics by category"""
    from inventory.models import Category
    
    stats = []
    for category in Category.objects.all():
        products = category.products.filter(is_active=True)
        stats.append({
            'category': category.name,
            'total_products': products.count(),
            'total_value': products.aggregate(
                total=Sum(F('price') * F('quantity'))
            )['total'] or 0
        })
    
    return stats


def export_to_json(data):
    """Convert data to JSON"""
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)
