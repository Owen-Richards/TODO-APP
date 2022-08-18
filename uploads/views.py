from django.shortcuts import render, redirect
from .models import photos
from .forms import PictureForm
from cloudinary.forms import cl_init_js_callbacks
def index(request):
    pictures=photos.objects.all()
    ctx={'pictures':pictures}
    return render(request,'pictures/index.html',ctx)
def loadPicture(request):
    if request.method=="POST":
        form=PictureForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    form=PictureForm()
    ctx={'form':form}
    return render(request, 'pictures/load.html',ctx)
# Create your views here.
