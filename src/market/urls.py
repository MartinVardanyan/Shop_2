from django.urls import path
from market import views
from market import admin_views
from market import customer_views

app_name = 'market'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/register/', admin_views.AdminRegisterView.as_view(), name='admin_register'),
    path('admin/profile/', admin_views.AdminProfileView.as_view(), name='admin_profile'),
    path('admin/stock/', admin_views.AdminStockView.check_view, name='my_stock'),
    path('admin/stock/<int:id>/', admin_views.AdminStockView.as_view(), name='edit_stock_name'),
    path('admin/category/<int:id>/', admin_views.AdminCategoryView.as_view(), name='category'),
    path('admin/stock/add/category/', admin_views.AdminCategoryView.check_view, name='add_category'),
    path('admin/stock/category/<int:id>/add/item/', admin_views.AdminItemView.as_view(), name='add_item'),
    path('admin/stock/category/item/<int:id>/edit/', admin_views.AdminItemView.check_view, name='edit_item'),
    path('admin/my/stock/income/', admin_views.Admin_Income_View.as_view(), name='income'),
    path('customer/register/', customer_views.Customer_Register_View.as_view(), name='customer_register'),
    path('customer/profile/', customer_views.Customer_Profile_View.as_view(), name='customer_profile'),
    path('customer/stocks/', customer_views.CustomerGetView.get_stock_list, name='stock_list'),
    path('customer/stock/<int:id>/categories/', customer_views.CustomerGetView.get_category_list, name='category_list'),
    path('customer/stock/category/<int:id>/items/', customer_views.CustomerGetView.get_item_list, name='item_list'),
    path('customer/my/bug/', customer_views.CustomerMyBugView.as_view(), name='my_bug'),
    path('customer/my/bug/add/item/<int:id>', customer_views.CustomerMyBugView.check_view, name='my_bug_add'),
    path('customer/remove/item/<int:id>/in/my/bug/', customer_views.CustomerMyBugView.remove, name='remove'),
]
