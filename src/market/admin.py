# django imports
from django.contrib import admin

# 3-th path imports
from market.models import Category, Item, Stock, MyBag, Administrator, Customer


#
class ItemAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'category_name', 'name', 'price', 'quanity', 'admin', 'customer', 'info', 'is_removed')
    empty_value_display = '-empty-'

    def stock_name(self, item):
        return item.name

    def category_name(self, item):
        return item.category.name + " " + item.stock.name


#
class StockAdmin(admin.ModelAdmin):
    list_display = ('admin_name', 'stock_name')
    empty_value_display = '-empty-'

    def admin_name(self, stock):
        return stock.admin.user

    def stock_name(self, stock):
        return stock.name


#
class MyBagAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item_name', 'buy_time')
    empty_value_display = '-empty-'

    def customer_name(self, my_bag):
        return my_bag.customer.user

    def item_name(self, my_bag):
        return my_bag.item.name, my_bag.item.quanity


#
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'registrated_at')
    empty_value_display = '-empty-'

    def user_name(self, administrator):
        return administrator.user


#
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'registrated_at')
    empty_value_display = '-empty-'

    def user_name(self, customer):
        return customer.user


#
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'stock_name')
    empty_value_display = '-empty-'

    def category_name(self, category):
        return category.name

    def stock_name(self, stock):
        return stock.stock.name


#
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(MyBag, MyBagAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Customer, CustomerAdmin)
