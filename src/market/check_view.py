'''
class MyViewClass(View):
    def get(self, request, x_id):
        pass

    def patch(self, request, x_id):
        obj = MyViewModel.objects.get(id=x_id)

        name = request.PATCH.get('name', None)
        field_1 = request.PATCH.get('field1', None)
        field_2 = request.PATCH.get('field2', None)

        if name:
            obj.name = name
        if field1:
            obj.field1 = field1
        if field_2:
            obj.field_2 = field2
        obj.save()'''

'''pass

    def delete(self, request, x_id):
        pass
    
    @staticmethod
    def check_view(request):
        if request.method == 'GET':
            MyViewClass.get_list(request)
        elif request.method == 'POST':
            MyViewClass.create_obj(request)
        else:
            return HttpResponseError("method not allowed")

    @staticmethod
    def get_list(request):
        pass

    @staticmethod
    def create_obj(request):
        pass 
'''