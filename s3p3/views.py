from django.shortcuts import render, redirect
from .models import Folder, PDF
from django.contrib.auth.decorators import login_required
from classes.models import ClassesAndStudents, Class

@login_required(login_url='/')
def gallery(request):
    getAllVals=ClassesAndStudents.objects.filter(student=request.user)
    classList=[i.Class for i in getAllVals]
    folder=request.GET.get('course')
    if folder==None:
        files=PDF.objects.filter(category__in=classList)
    else:
        files=PDF.objects.filter(category__name=folder)
    courses=ClassesAndStudents.objects.filter(student=request.user)
    context={'courses': courses, 'pdfs':files}
    return render(request, 'pdf/gallery.html', context)

@login_required(login_url='/')
def addpdf(request):
    courses=ClassesAndStudents.objects.filter(student=request.user)
    if(request.method=='POST'):
        data=request.POST
        print(data)
        file=request.FILES.get('pdf')
        finClass=Class.objects.get(id=data['course'])
        pdf = PDF.objects.create(
            category=finClass,
            description=data['description'],
            PDF=file,
            student=request.user
        )
        return redirect('gallery')

    context={'courses': courses}
    return render(request, 'pdf/add.html', context)

@login_required(login_url='/')
def viewpdf(request, pk):
    pdf=PDF.objects.get(id=pk)
    return render(request, 'pdf/photo.html', {'pdf': pdf})

@login_required(login_url='/')
def deletePDF(request):
    pdfs=PDF.objects.filter(student=request.user)
    if(request.method=='POST'):
        data=request.POST
        PDF.objects.get(id=data['course']).delete()
        return redirect('gallery')
    return render(request, 'pdf/deletePDF.html', {'pdfs': pdfs})

# Create your views here.
