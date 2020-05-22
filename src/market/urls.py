from django.urls import path
from market import views
from market import admin_views
from market import customer_views

app_name = 'market'

urlpatterns = [
    path('', views.Login_View.as_view(), name='login'),
    path('admin_register/', admin_views.Admin_Register_View.as_view(), name='admin_register'),
    path('customer_register/', customer_views.Customer_Register_View.as_view(), name='customer_register'),
    path('login/', views.Logout_View.as_view(), name='logout'),
    path('admin_profile/', admin_views.Admin_Profile_View.as_view(), name='admin_profile'),
    path('my_stock/', admin_views.Admin_Stock_View.as_view(), name='my_stock'),
    path('my_stock/add_category/', admin_views.Admin_Add_Category_View.as_view(), name='add_category'),
    path('my_stock/category/<int:id>/add_item/', admin_views.Admin_Add_Item_View.as_view(), name='add_item'),
    path('category/<int:id>/', admin_views.Admin_Category_View.as_view(), name='category'),
    path('my_stock/edit_stock_name/<int:id>/', admin_views.Admin_Edit_Stock_Name_View.as_view(), name='edit_stock_name'),
    path('my_stock/category/<int:id>/edit_category_name/', admin_views.Admin_Edit_Category_Name_View.as_view(), name='edit_category_name'),
    path('category/<int:id>/edit_item_name/', admin_views.Admin_Edit_Item_Name_View.as_view(), name='edit_item_name'),
    path('category/<int:id>/edit_item_price/', admin_views.Admin_Edit_Item_Price_View.as_view(), name='edit_item_price'),
    path('category/<int:id>/edit_item_quanity/', admin_views.Admin_Edit_Item_Quanity_View.as_view(), name='edit_item_quanity'),
    path('my_stock/income/', admin_views.Admin_Income_View.as_view(), name='income'),
    path('customer_profile/', customer_views.Customer_Profile_View.as_view(), name='customer_profile'),
    path('customer/stock_list/', customer_views.Customer_Stock_List_View.as_view(), name='stock_list'),
    path('customer/stock/<int:id>/category_list/', customer_views.Customer_Stock_Category_List_View.as_view(), name='category_list'),
    path('customer/stock/category/<int:id>/item_list/', customer_views.Customer_Stock_Category_Item_List_View.as_view(), name='item_list'),
    path('customer/add_item/<int:id>/in_my_bug/', customer_views.Customer_Add_Item_MyBug_View.as_view(), name='add_item_in_my_bug'),
    path('customer/my_bug/', customer_views.Customer_MyBug_View.as_view(), name='my_bug'),
    path('customer/remove_item/<int:id>/in_my_bug/', customer_views.Customer_Remove_MyBug_Item_View.as_view(), name='remove_item_in_my_bug'),

    # path('valod.id', Class.as_view())
    # path('valod', Class.my_func)
]


    #
#    @staticmethod
#    def check_view(request):
#        if request.method == 'GET':
#            return ASActivityView.get_list(request)
#        elif request.method == 'POST':
#            return ASActivityView.create_obj(request)
