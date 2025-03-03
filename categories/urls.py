from django.urls import path
from categories import views

urlpatterns = [
    path("", views.CategoriesList.as_view(), name="categories"),
    path("<int:pk>/", views.CategoryDetail.as_view(), name="category"),
]
