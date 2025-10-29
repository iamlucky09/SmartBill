from django.shortcuts import render,redirect
from .models import User
from .forms import AddUserForm
# Create your views here.
def add_user(request):
    if request.method=='POST':
        form=AddUserForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('form_list')
    else:
        form=AddUserForm()

    return render(request,"forms/add_user_form.html",{"form":form}) 