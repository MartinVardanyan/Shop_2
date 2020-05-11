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
    path('my_stock/edit_stock_name/<int:id>/', AdminViews.AdminEditStockNameView.as_view(), name='edit_stock_name'),
    path('my_stock/category/<int:id>/edit_category_name/', AdminViews.AdminEditCategoryNameView.as_view(), name='edit_category_name'),
    path('category/<int:id>/edit_item_name/', AdminViews.AdminEditItemNameView.as_view(), name='edit_item_name'),
    path('category/<int:id>/edit_item_price/', AdminViews.AdminEditItemPriceView.as_view(), name='edit_item_price'),
    path('category/<int:id>/edit_item_quanity/', AdminViews.AdminEditItemQuanityView.as_view(), name='edit_item_quanity'),
    path('my_stock/income/', AdminViews.AdminIncomeView.as_view(), name='income'),
    path('customer_profile/', CustomerViews.CustomerProfileView.as_view(), name='customer_profile'),
    path('customer/stock_list/', CustomerViews.CustomerStockListView.as_view(), name='stock_list'),
    path('customer/stock/<int:id>/category_list/', CustomerViews.CustomerStockCategoryListView.as_view(), name='category_list'),
    path('customer/stock/category/<int:id>/item_list/', CustomerViews.CustomerStockCategoryItemListView.as_view(), name='item_list'),
]
