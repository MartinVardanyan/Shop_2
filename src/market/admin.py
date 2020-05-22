from django.contrib import admin
from market.models import Category, Item, Stock, MyBug, Administrator, Customer


class ItemAdmin(admin.ModelAdmin):
    list_display = ('stock', 'category', 'name', 'price', 'quanity', 'full_name', 'customer')

    def full_name(): # some params
        return admin.user.first_name + " " + admin.user.last_name

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/



class StockAdmin(admin.ModelAdmin):
    list_display = ('admin', 'name')


class MyBugAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'buy_time')


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'registrated_at')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'registrated_at')


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Stock, StockAdmin)
admin.site.register(MyBug, MyBugAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Customer, CustomerAdmin)
