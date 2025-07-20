
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Assignment, Submission
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import datetime
# Create your views here.
# Home Page
def home(request):
    qs=Assignment.objects.all()
    context={
        'assignments':qs
    }
    return render(request, 'tracker/home.html',context)


#  SIGNUP VIEW
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if role not in ['teacher', 'student']:
            return JsonResponse({'error': 'Invalid role'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, role=role)
        return redirect('login')

    return render(request, 'tracker/signup.html')


#  LOGIN VIEW
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})

    return render(request, 'tracker/login.html')


#  LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


#  CREATE ASSIGNMENT 
@login_required
def create_assignment(request):
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Only teachers can create assignments'}, status=403)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']  

        assignment = Assignment.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            created_by=request.user
        )
        return redirect('home')

    return render(request, 'tracker/create_assignment.html')


#  SUBMIT ASSIGNMENT 
@login_required
def submit_assignment(request, assignment_id):
    if request.user.role != 'student':
        return JsonResponse({'error': 'Only students can submit assignments'}, status=403)

    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        content = request.POST['content']
        file = request.FILES.get('file', None)

        Submission.objects.create(
            assignment=assignment,
            submitted_by=request.user,
            content=content,
            file=file
        )
        return redirect('home')

    return render(request, 'tracker/submit_assignment.html', {'assignment': assignment})


#  VIEW SUBMISSIONS 
@login_required
def view_submissions(request, user_id):
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Only teachers can view submissions'}, status=403)

    # assignment = get_object_or_404(Assignment, id=assignment_id)
    # submissions = Submission.objects.filter(assignment=assignment)

    # return render(request, 'tracker/view_submissions.html', {
    #     'assignment': assignment,
    #     'submissions': submissions
    # })
    assignment=Assignment.objects.filter(created_by=user_id)
    students=[]
    assi_title=assignment[0].title
    for i in assignment:
        stu=Submission.objects.filter(assignment=i.id)
        students.append(stu)
    #print(students)
    return render(request,'tracker/view_submissions.html',{'students':students,'assignment':assi_title})

