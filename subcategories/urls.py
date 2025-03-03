from django.urls import path
from subcategories import views

urlpatterns = [
    path("", views.SubCategoriesList.as_view(), name="subcategories"),
    path("<int:pk>/", views.SubCategoryDetail.as_view(), name="subcategory"),
]
