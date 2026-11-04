from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Student

User = get_user_model()

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())
@csrf_exempt
def signup(request):
    template = loader.get_template("signup.html")
    return HttpResponse(template.render())
@csrf_exempt
def registerStudent(request):
    if request.method == "POST":
        mail = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        if User.objects.filter(username=mail).exists():
            return render(request, "signup.html", {
                'error': 'This email address is already registered.'
            })
        user = User.objects.create_user(
            username=mail,
            email=mail,
            password=password
        )
        s = Student(
            user=user,
            first_name=request.POST.get('firstName'),
            last_name=request.POST.get('lastName'),
            student_id=request.POST.get('studentId'),
            email_address=mail,
            fields_of_study=request.POST.get('field'),
            classification=request.POST.get('year'),
        )
        s.save()
        login(request, user)
        return redirect("/students")

    return render(request, "signup.html")
def createFaculty(request):
    return HttpResponseRedirect("/")
def student_list(request):
    template = loader.get_template("students.html")
    allStudents = Student.objects.all().values()
    context = {'allStudents': allStudents}
    return HttpResponse(template.render(context, request))
