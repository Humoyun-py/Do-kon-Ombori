"""
Django management command to create initial data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Role, Category, Supplier, Product, UserProfile


class Command(BaseCommand):
    help = 'Boshlang\'ich ma\'lumotlarni yaratadi'

    def handle(self, *args, **options):
        self.stdout.write('Boshlang\'ich ma\'lumotlar yaratilmoqda...')
        
        # Create roles
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Administratsiya'}
        )
        warehouse_role, _ = Role.objects.get_or_create(
            name='warehouseman',
            defaults={'description': 'Omborchi'}
        )
        staff_role, _ = Role.objects.get_or_create(
            name='staff',
            defaults={'description': 'Do\'kon xodimi'}
        )
        
        # Create categories
        categories_data = [
            ('Oziq-ovqat', 'Oziq-ovqat mahsulotlari'),
            ('Ichimliklar', 'Har xil ichimliklar'),
            ('Cleanliness', 'Tozalash vositalari'),
            ('Elektronika', 'Elektron jihozlar'),
            ('Poyabzal', 'Ayakkabiler va poyabzallar'),
        ]
        
        for name, description in categories_data:
            Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
        
        # Create suppliers
        suppliers_data = [
            {
                'name': 'Global Supplier',
                'contact_person': 'Ali Rizo\'ev',
                'phone_number': '+998901234567',
                'address': 'Toshkent, Mirobod tumanida',
                'city': 'Toshkent'
            },
            {
                'name': 'Lokal Company',
                'contact_person': 'Sobirjon Hasanov',
                'phone_number': '+998901234568',
                'address': 'Samarqand, Registan tumani',
                'city': 'Samarqand'
            }
        ]
        
        for supplier_data in suppliers_data:
            Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults={
                    'contact_person': supplier_data['contact_person'],
                    'phone_number': supplier_data['phone_number'],
                    'address': supplier_data['address'],
                    'city': supplier_data['city']
                }
            )
        
        # Create sample products
        food_category = Category.objects.get(name='Oziq-ovqat')
        supplier = Supplier.objects.first()
        
        products_data = [
            {
                'name': 'Non',
                'code': 'FOOD001',
                'category': food_category,
                'supplier': supplier,
                'price': '3000.00',
                'quantity': 50,
                'unit': 'dona',
                'min_stock': 20,
            },
            {
                'name': 'Alik sut',
                'code': 'FOOD002',
                'category': food_category,
                'supplier': supplier,
                'price': '5500.00',
                'quantity': 30,
                'unit': 'dona',
                'min_stock': 15,
            },
            {
                'name': 'Guruch',
                'code': 'FOOD003',
                'category': food_category,
                'supplier': supplier,
                'price': '8000.00',
                'quantity': 100,
                'unit': 'kg',
                'min_stock': 50,
            },
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                code=product_data['code'],
                defaults=product_data
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Boshlang\'ich ma\'lumotlar muvaffaqiyatli yaratildi!'))
