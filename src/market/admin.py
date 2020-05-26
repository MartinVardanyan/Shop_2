from django.contrib import admin

from market.models import Category, Item, Stock, MyBug, Administrator, Customer


class ItemAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('stock_name', 'category_name', 'name', 'price', 'quanity', 'admin', 'customer')
    empty_value_display = '-empty-'

    def stock_name(self, item):
        return item.name

    def category_name(self, item):
        return item.category.name + " " + item.stock.name
=======
    list_display = ('stock', 'category', 'name', 'price', 'quanity', 'full_name', 'customer')

    def full_name(): # some params
        return admin.user.first_name + " " + admin.user.last_name

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/

>>>>>>> 6504ac7a4f2a6a47b483f7e7b0fcb12a564cbf8d


class StockAdmin(admin.ModelAdmin):
    list_display = ('admin_name', 'stock_name')
    empty_value_display = '-empty-'

    def admin_name(self, stock):
        return stock.admin.user

    def stock_name(self, stock):
        return stock.name


class MyBugAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item_name', 'buy_time')
    empty_value_display = '-empty-'

    def customer_name(self, my_bug):
        return my_bug.customer.user

    def item_name(self, my_bug):
        return my_bug.item.name, my_bug.item.quanity


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'registrated_at')
    empty_value_display = '-empty-'

    def user_name(self, administrator):
        return administrator.user


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'registrated_at')
    empty_value_display = '-empty-'

    def user_name(self, customer):
        return customer.user


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'stock_name')
    empty_value_display = '-empty-'

    def category_name(self, category):
        return category.name

    def stock_name(self, stock):
        return stock.stock.name


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(MyBug, MyBugAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Customer, CustomerAdmin)
