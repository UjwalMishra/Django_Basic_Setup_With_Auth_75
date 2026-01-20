from django.http import JsonResponse
from .models import Product
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages




def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")

        if not request.user.is_staff:
            raise PermissionDenied  # 🔥 403 Forbidden

        return view_func(request, *args, **kwargs)

    return wrapper




def signup(request) : 
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/products/")
    else :
        form = UserCreationForm()
            
    return render(request, "registration/signup.html",{
        "form": form
    })


@login_required
def get_products(request):
    products = Product.objects.all()
    return render(request, "products/list.html",{
        "products": products
    })
    
@login_required
@admin_required
def post_products(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        
        if not name or not price or not quantity:
            return JsonResponse(
                {"error": "name, price and quantity are required"},
                status=400
            )
        
        product = Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )
        messages.success(request, "Product created successfully")
        return redirect("/products/")
    
    return render(request, "products/create.html")

@login_required
@admin_required
def update_products(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        
        if name : 
            product.name = name
        if price : 
            product.price = price
        if quantity : 
            product.quantity = quantity

        product.save()
        messages.success(request, "Product updated successfully")
        return redirect("/products/")

    return render(request, "products/update.html", {
        "product": product
    })

@login_required
@admin_required
def delete_products(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect("/products/")

    return render(request, "products/delete.html", {
        "product": product
    })