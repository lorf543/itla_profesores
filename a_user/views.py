from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def loging_view(request):
    context ={
        
    }
    return render(request,'a_user/longin.html',context)