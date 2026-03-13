"""
Views for inventory app
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count, F
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Product, Category, Transaction, Stock, Supplier, Notification, Report
from .forms import ProductForm, TransactionForm, CategoryForm


class DashboardView(LoginRequiredMixin, ListView):
    """Main dashboard view"""
    template_name = 'inventory/dashboard.html'
    context_object_name = 'products'
    login_url = 'login'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Overview statistics
        context['total_products'] = Product.objects.count()
        context['low_stock_products'] = Product.objects.filter(
            quantity__lt=F('min_stock')
        ).count()
        context['out_of_stock'] = Product.objects.filter(quantity=0).count()
        
        # Revenue calculations
        last_30_days = datetime.now() - timedelta(days=30)
        context['income_transactions'] = Transaction.objects.filter(
            transaction_type='income',
            created_at__gte=last_30_days
        ).count()
        
        context['categories'] = Category.objects.all()
        context['recent_transactions'] = Transaction.objects.all()[:5]
        
        return context


@login_required
def product_list(request):
    """List all products"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        products = products.filter(category_id=category)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'query': query,
        'selected_category': category
    }
    return render(request, 'inventory/product_list.html', context)


@login_required
def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    transactions = product.transactions.all()[:20]
    
    context = {
        'product': product,
        'transactions': transactions
    }
    return render(request, 'inventory/product_detail.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Create new product"""
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Update product"""
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Delete product"""
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


@login_required
def add_transaction(request, product_id):
    """Add income/outcome transaction"""
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.created_by = request.user
            transaction.save()
            
            # Update product quantity
            if transaction.transaction_type == 'income':
                product.quantity += transaction.quantity
            else:  # outcome
                product.quantity -= transaction.quantity
            product.save()
            
            return redirect('product_detail', pk=product_id)
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'inventory/add_transaction.html', context)


@login_required
def stock_report(request):
    """Stock report view"""
    products = Product.objects.annotate(
        total_transactions=Count('transactions')
    ).order_by('-total_transactions')
    
    low_stock = products.filter(quantity__lt=F('min_stock'))
    out_of_stock = products.filter(quantity=0)
    
    context = {
        'products': products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'total_products': products.count()
    }
    return render(request, 'inventory/stock_report.html', context)


@login_required
def transaction_report(request):
    """Transaction history report"""
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    trans_type = request.GET.get('type', '')
    
    transactions = Transaction.objects.all()
    
    if start_date:
        transactions = transactions.filter(created_at__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__date__lte=end_date)
    if trans_type:
        transactions = transactions.filter(transaction_type=trans_type)
    
    context = {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'inventory/transaction_report.html', context)
