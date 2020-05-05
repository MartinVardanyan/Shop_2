from django.urls import path
from market import views
from market import AdminViews
from market import CustomerViews

app_name = 'market'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('admin_register/', AdminViews.AdminRegisterView.as_view(), name='admin_register'),
    path('customer_register/', CustomerViews.CustomerRegisterView.as_view(), name='customer_register'),
    path('login/', views.LogoutView.as_view(), name='logout'),
    path('admin_profile/', AdminViews.AdminProfileView.as_view(), name='admin_profile'),
    path('my_stock/', AdminViews.AdminStockView.as_view(), name='my_stock'),
    path('my_stock/add_category/', AdminViews.AdminAddCategoryView.as_view(), name='add_category'),
    path('my_stock/category/<int:id>/add_item/', AdminViews.AdminAddItemView.as_view(), name='add_item'),
    path('category/<int:id>/', AdminViews.AdminCategoryView.as_view(), name='category'),
]
