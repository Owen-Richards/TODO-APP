from django.shortcuts import render, redirect
from .models import *
from s3p3.models import PDF
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required(login_url='/')
def viewAllClasses(request):
    classes=ClassesAndStudents.objects.filter(student=request.user)
    ctx={'classes': classes}
    return render(request, 'class/classroom.html', ctx)

@login_required(login_url='/')
def addClass(request):
    classes=Class.objects.all()
    if(request.POST):
        data=request.POST
        if ClassesAndStudents.objects.filter(Class = data['class'], student=request.user).exists():
            return redirect('classes')
        userandclass = ClassesAndStudents.objects.create(
            student=request.user,
            Class=Class.objects.get(id=data['class'])
        )
        return redirect('classes')
    ctx={'classes': classes}
    return render(request, 'class/addClass.html', ctx)
    
@login_required(login_url='/')
def viewClass(request, pk):
    posts=Message.objects.filter(Class__id=pk)
    classes=ClassesAndStudents.objects.filter(Class__id=pk)
    classFiles=PDF.objects.filter(category__id=pk)

    return render(request, 'class/viewClass.html', {'classes': classes, 'pdfs': classFiles, 'posts': posts})
@login_required(login_url='/')
def deleteClass(request,pk):
    toBeDeleted=ClassesAndStudents.objects.get(student=request.user, Class__id=pk)
    toBeDeleted.delete()
    return redirect('classes')
@login_required(login_url='/')
def postMessage(request, pk):
    if(request.POST):
        data=request.POST
        newMessage=Message.objects.create(
            student=request.user,
            Class=Class.objects.get(pk=pk),
            title=data['title'],
            text=data['body']
        )
        return redirect('viewClass', pk=pk)
    return render(request, 'class/postMessage.html')
@login_required(login_url='/')
def viewMessage(request, pk):
    message=Message.objects.get(pk=pk)
    comments=Comment.objects.filter(message__id=pk)
    if(request.POST):
        data=request.POST
        newComm=Comment.objects.create(
            student=request.user,
            message=message,
            text=data['commentbody']
        )
        return redirect('viewMessage', pk=pk)
    
    return render(request, 'class/viewMessage.html', {'message': message, 'comments': comments})
