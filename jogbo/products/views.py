from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.db.models import Sum

# Create your views here.
def list(request):
    products = Product.objects.all()
    add = Product.objects.all().aggregate(Sum('add_money'))['add_money__sum']
    use = Product.objects.all().aggregate(Sum('use_money'))['use_money__sum']
    now = Product.objects.all().aggregate(Sum('money'))['money__sum']
    return render(request, 'products/list.html', {'products': products, 'add': add, 'use':use, 'now':now})


def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        use_money = int(request.POST.get('use_money'))
        add_money = int(request.POST.get('add_money'))
        money = add_money - use_money
        description = request.POST.get('description')
        product = Product.objects.create(title=title, money=money, use_money=use_money, add_money=add_money, description=description)
        return redirect('list')
    return render(request, 'products/create.html')
    

def show(request, id):
    product = get_object_or_404(Product, pk =id)
    product.save()
    return render(request, 'products/show.html', {'product':product})


def edit(request, id):
    product = get_object_or_404(Product, pk =id)
    return render(request, 'products/edit.html', {'product': product})


def update(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk =id)
        title = request.POST.get('title')
        use_money = int(request.POST.get('use_money'))
        add_money = int(request.POST.get('add_money'))
        money = add_money - use_money
        description = request.POST.get('description')
        product.title = title
        product.money = money
        product.use_money = use_money
        product.add_money = add_money
        product.description = description
        product.save()
        return redirect('products:show', product.pk)
        
        
def delete(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk =id)
        product.delete()
        return redirect('list')