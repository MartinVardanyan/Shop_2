# django imports
from django.urls import path

# 3-th part imports
from market import views
from market import admin_views
from market import customer_views

app_name = 'market'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/contacts', views.AdminContactsView.as_view(), name='contacts_for_admin'),
    path('admin/about', views.AdminAboutView.as_view(), name='about_for_admin'),
    path('admin/register/', admin_views.AdminRegisterView.as_view(), name='admin_register'),
    path('admin/profile/', admin_views.AdminProfileView.as_view(), name='admin_profile'),
    path('admin/stock/', admin_views.AdminStockView.check_view, name='my_stock'),
    path('admin/stock/<int:id>/', admin_views.AdminStockView.as_view(), name='edit_stock_name'),
    path('admin/category/<int:id>/', admin_views.AdminCategoryView.as_view(), name='category'),
    path('admin/stock/category/add/', admin_views.AdminCategoryView.check_view, name='add_category'),
    path('admin/stock/category/<int:id>/item/add/', admin_views.AdminItemView.as_view(), name='add_item'),
    path('admin/stock/category/item/<int:id>/edit/', admin_views.AdminItemView.check_view, name='edit_item'),
    path('admin/my/stock/income/', admin_views.AdminIncomeView.as_view(), name='income'),
    path('customer/contacts', views.CustomerContactsView.as_view(), name='contacts_for_customer'),
    path('customer/about', views.CustomerAboutView.as_view(), name='about_for_customer'),
    path('customer/register/', customer_views.CustomerRegisterView.as_view(), name='customer_register'),
    path('customer/profile/', customer_views.CustomerProfileView.as_view(), name='customer_profile'),
    path('customer/stocks/', customer_views.CustomerGetView.get_stock_list, name='stock_list'),
    path('customer/stock/<int:id>/categories/', customer_views.CustomerGetView.get_category_list, name='category_list'),
    path('customer/stock/category/<int:id>/items/', customer_views.CustomerGetView.get_item_list, name='item_list'),
    path('customer/bug/', customer_views.CustomerMyBagView.as_view(), name='my_bag'),
    path('customer/bug/item/<int:id>/add/', customer_views.CustomerMyBagView.check_view, name='my_bag_add'),
    path('customer/bug/item/<int:id>/remove/', customer_views.CustomerMyBagView.remove, name='remove'),
]
