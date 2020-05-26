'''from django.urls import path
from market import views
from market import admin_views
from market import customer_views

app_name = 'market'

urlpatterns = [
    path('valod/id', MyViewClass.as_view())
    path('valod', MyViewClass.check_view)
]


    #
#    @staticmethod
#    def check_view(request):
#        if request.method == 'GET':
#            return ASActivityView.get_list(request)
#        elif request.method == 'POST':
#            return ASActivityView.create_obj(request)
'''