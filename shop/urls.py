from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-listing/step2/', views.add_listing_step2, name='add_listing_step2'), # Жаңы кадам
    path('add-listing/submit/', views.add_product_public, name='add_product_public'),
# Бул эки саптыurlpatterns тизмесинин ичине кошуңуз:
    path('product/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('product/<int:pk>/delete/', views.delete_listing, name='delete_listing'),

]
