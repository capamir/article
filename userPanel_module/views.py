from django.shortcuts import render
from  django.views import View
# Create your views here.

class StudentView(View):
    def get(self, request):
        context = {}
        return render(request, 'userPanel_module/studentView.html', context)
    def post(self, request):
        pass