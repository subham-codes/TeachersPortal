import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from .models import StudentModel
# Create your views here.

logger = logging.getLogger('mylogger')
    
@login_required(login_url='student_listing:login')
def home(request):
    logger.info('Home view starts:'+ str(request.method))
    try:
        if request.method == 'GET':
            search = request.GET.get('search')
            if search:
                stu_obj = StudentModel.objects.filter(name=search).order_by('id')
            else:
                stu_obj = StudentModel.objects.all().order_by('id')

            # pagination logic
            paginator = Paginator(stu_obj, 10)
            page_number = request.GET.get('page') if request.GET.get('page') else 1
            page_obj = paginator.get_page(page_number)

            logger.info('Student data fetched')
            logger.info('Home view ends:'+ str(request.method))
            return render(request, 'student_listing/home.html', {'page_obj': page_obj,
                                                             'search':search})
        
        # for adding records
        if request.method == 'POST':
            rows = json.loads(request.POST.get('rows', '[]'))
            for row in rows:
                name=row['name'].strip().lower()
                subject=row['subject'].strip().lower()
                mark=row['marks']

                # if student name and subject matches, get the object else create new one
                get_obj, created = StudentModel.objects.get_or_create(
                                        name=name,
                                        subject=subject,
                                        defaults={'mark': mark}
                                    )

                # if record is already present, update the marks
                if not created:
                    if get_obj.mark != row['marks']:  # if marks are different
                        get_obj.mark = row['marks']
                        get_obj.save()


            messages.success(request, 'Student data successfully added')
            logger.info('Student data successfully added')
            logger.info('Home page ends:'+ str(request.method))
            return JsonResponse({'success': True})
        
    except Exception as exe:
        logger.error('Error occurred at home view'+str(exe))
    

# @login_required(login_url='student_listing:login')
def delete_student(request,id=None):
    logger.info('delete_student view starts:'+str(request.method))
    try:
        if request.method == 'GET':
            search = request.GET.get('search') if request.GET.get('search') else ''
            page = request.GET.get('page')  
            stu_obj = StudentModel.objects.filter(id=id).first()
            if stu_obj:
                stu_obj.delete()

            messages.success(request, 'User deleted successfully')
            url = reverse('student_listing:home')

            logger.info('User deleted')
            logger.info('delete_student view ends: '+str(request.method))
            return redirect(f"{url}?search={search}&page={page.strip()}")
        
    except Exception as exe:
        logger.error('Error occurred at delete_student view: '+str(exe))
        
        
    
@login_required(login_url='student_listing:login')
def update_student(request,id=None):
    logger.info('update_student view starts:' + str(request.method))
    try:
        if request.method == 'POST':
            print('update function')
            stu_obj = StudentModel.objects.filter(id=id).first()
            marks = int(request.POST.get("marks"))

            if marks < 0 or marks > 100:
                logger.error('Marks must be between 0 and 100.')
                return JsonResponse({'error':'Marks must be between 0 and 100.'})

            if stu_obj:
                stu_obj.name = request.POST.get("name")
                stu_obj.subject = request.POST.get("subject")
                stu_obj.mark = marks
                stu_obj.save()

            messages.success(request, 'User updated successfully')
            logger.info('User updated successfully')
            logger.info('update_student view ends')

            return JsonResponse({'success':'Updated'})

    except Exception as exe:
        logger.error('Error occured at update_student view: '+str(exe))



def register(request):
    logger.info('register view starts:'+ str(request.method))
    try:
        # for user register
        if request.method == 'POST':
            username = request.POST.get('username')
            fname = request.POST.get('fname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            # password2 = request.POST.get('password2')

            if User.objects.filter(username=username).exists():
                error_msg="User already exists"
                logger.error('User already exists')
                return render(request,'student_listing/register.html',{'error':error_msg})
            
            user = User.objects.create_user(username=username,first_name=fname,email=email,password=password)
            messages.success(request, 'User created successfully')
            logger.info('User created successfully')
            logger.info('register view ends'+str(request.method))
            return redirect('student_listing:login')
        
        # for accessing register page
        logger.info('register view ends'+ str(request.method))
        return render(request,'student_listing/register.html')
    
    except Exception as exe:
        logger.error('Error occured at register view: '+str(exe))



def login(request):
    logger.info('Login page starts: '+ str(request.method))
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    logger.info('User logged in')
                    auth_login(request, user)
                    messages.success(request, 'User Logged In successfully')
                    return redirect('student_listing:home')
                else:
                    logger.error('Login failed: Invalid username or password')
                    messages.error(request, 'Invalid username or password')
                    return render(request, 'student_listing/login.html', {'error': 'Invalid username or password'})
            else:
                logger.error('Login failed: Username or password not found')
                return render(request, 'student_listing/login.html', {'error': 'username or password not found'})
        
        logger.info('Login view ends'+ str(request.method))
        return render(request, 'student_listing/login.html')
    
    except Exception as e:
        logger.error('Something went wrong '+str(e))


def logout_view(request):
    logger.info('logout_view starts: '+str(request.method))
    try:

        logout(request)

        messages.success(request, 'User Logged out successfully')
        logger.info('User Logged out successfully')
        logger.info('logout_view ends')

        return redirect('student_listing:login')
    except Exception as exe:
        logger.error('Error occured at logout_view' + str(exe))
    