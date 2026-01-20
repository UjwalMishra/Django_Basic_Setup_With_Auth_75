from django.urls import path
from .views import get_products, post_products, update_products, delete_products

urlpatterns = [
    path("", get_products),           
    path("create/", post_products),
    path("update/<int:id>/", update_products),
    path("delete/<int:id>/", delete_products)  
]
    

