from django.urls import path
from products import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="products"),
    path("<int:pk>/", views.ProductDetail.as_view(), name="product"),
]
