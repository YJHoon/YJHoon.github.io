from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('create/', views.create, name="create"),
    path('<int:id>/', views.show, name="show"),
    path('edit<int:id>/', views.edit, name="edit"),
    path('update/<int:id>/', views.update, name="update"),
    path('delete/<int:id>/', views.delete, name="delete"),
]