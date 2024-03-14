import uuid
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Admin, Help,CourseFaculty, Meetings, Sections, Semesters, User, users,Faculty,Students,Rooms,Courses,Table,Classes
import datetime,os,pytz,ast
from django.db import IntegrityError
import math
from django.http import JsonResponse
from  Automatic_Timetable_Generator import settings
from .models import Faculty,UploadedFile,Certificate
from .models import FreferenceEnable
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.files import File
from django.http import HttpResponse
from django.contrib.auth import logout
import random
from .helpers import send_forget_password_mail
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05
# Create your views here.
# Home Views
def Home(request):
    return render(request,'Home/Home.html')
def signupOptions(request):
        semester= Semesters.objects.all()
        section= Sections.objects.all()
        context = {
        'semester': semester,
        'section':section,
            }
        return render(request,'Home/signupOptions.html',context)
def Quicktour(request):
    return render(request,'Home/Quicktour.html')
def Aboutus(request):
    return render(request,'Home/Aboutus.html')
def Contactus(request):
    return render(request,'Home/Contactus.html')
def Contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject1 = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = [settings.EMAIL_HOST_USER]
        subject = subject1
        from_email = email

        description = f'{name} is contacting you. {message}'

        if send_mail(subject, description, from_email, recipient_list, fail_silently=True):
            messages.success(request, "Thank you for your message. We will get back to you soon!")
            return JsonResponse({'status': 'success'})
        else:
            messages.error(request, "Oops! An error occurred while sending the email. Please try again.")
            return JsonResponse({'error_message': error_message})

def help(request):
    return render(request,'Home/help.html')
def ChangePassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        faculty = Faculty.objects.filter(u_email=email).first()
        student = Students.objects.filter(u_email=email).first()
        admin = Admin.objects.filter(u_email=email).first()
        if faculty:
            password1 = request.POST.get('password1')
            faculty.u_password = password1
            faculty.save()
            messages.success(request, 'Password has been changed.')
            return render(request, 'Home/ChangePassword.html')
        elif student:
            password1 = request.POST.get('password1')
            student.u_password = password1
            student.save()
            messages.success(request, 'Password has been changed.')
            return render(request, 'Home/ChangePassword.html')
        elif admin:
            password1 = request.POST.get('password1')
            admin.u_password = password1
            admin.save()
            messages.success(request, 'Password has been changed.')
            return render(request, 'Home/ChangePassword.html')
        else:
            messages.error(request, 'User not found.')
            return render(request, 'Home/ChangePassword.html')
    else:
        return render(request, 'Home/ChangePassword.html')

def ForgetPassword(request):
    return render(request,'Home/ForgetPassword.html')
def FormForgetPassword(request):
    if request.method=="POST":
        email= request.POST.get('email')
        if not (Faculty.objects.filter(u_email=email).exists() | Students.objects.filter(u_email=email).exists() | Admin.objects.filter(u_email=email).exists()):
            messages.success(request, 'Not user found with this email')
            return render(request,'Home/ForgetPassword.html')
        else:
            from_email=settings.EMAIL_HOST_USER
            subject='Password Reset Request'
            recipent_list= email
            # print(recipent_list)
            # print(from_email)
            # print(subject)
            # print(recipent_list)
            description='' 
            description +='Dear Madam,\n' 
            description +='We hope this message finds you well. You have requested to reset your password. Please use the following link to reset your password: http://127.0.0.1:8000/ChangePassword.html\n' 
            description +='If you did not make this request, please ignore this email.\n' 
            description +='Thank you.\n' 
            description +='Best regards,\n' 
            print(description)
            if send_mail(subject, description, from_email, [email], fail_silently=True):
                messages.success(request, "An email has been sent to your registered email address. Please check your email and follow the instructions to reset your password.")
            # return JsonResponse({'status': 'success'})
            return render(request, 'Home/ForgetPassword.html')
#signup views
#admin
def signup_admin(request):
    if request.method=="POST":
        a_name=request.POST.get('a_name');
        a_email=request.POST.get('a_email');
        a_gender=request.POST.get('a_gender');
        a_department=request.POST.get('a_department');
        a_password=request.POST.get('a_password');
        try:
            existing_admin= users.objects.filter(v_email=a_email, v_password=a_password)
            if not existing_admin:
                messages.error(request, "Email or Password is not match")
                return JsonResponse({'status': 'error'})
            else:
              save_admin=Admin(u_name=a_name,u_email=a_email,u_gender=a_gender,u_department=a_department,u_password=a_password)
              save_admin.save(); 
              request.session['user_id'] = save_admin.id
              messages.success(request, 'Registered successfully.')
              return JsonResponse({'status': 'success'})
        except users.DoesNotExist:
            messages.error(request, "Email does not exist")
            print("Email does not exist")
            return redirect('/')
    return render(request, 'Home/Home.html')
    
    

#faculty

def signup_faculty(request):
    if request.method=="POST":
        f_name=request.POST.get('f_name');
        f_email=request.POST.get('f_email');
        f_gender=request.POST.get('f_gender');
        f_department=request.POST.get('f_department');
        f_password=request.POST.get('f_password');
        try:
            existing_faculty= users.objects.filter(v_email=f_email, v_password=f_password)
            if not existing_faculty:
                messages.error(request,'Email or Password is not matched' )
                return JsonResponse({'status': 'error'})
            else:
              save_faculty=Faculty(u_name=f_name,u_email=f_email,u_gender=f_gender,u_department=f_department,u_password=f_password)
              save_faculty.save(); 
              request.session['user_idf'] = save_faculty.id
              messages.success(request, 'Registered successfully.')
              return JsonResponse({'status': 'success'})
        except users.DoesNotExist:
            messages.error(request, "Email does not exist")
            print("Email does not exist")
            return redirect('/')
    return render(request, 'Home/Home.html')

#student
def signup_student(request):
    if request.method=="POST":
        s_name=request.POST.get('s_name');
        s_email=request.POST.get('s_email');
        s_gender=request.POST.get('s_gender');
        s_password=request.POST.get('s_password');
        s_section=request.POST.get('s_section');
        s_semester=request.POST.get('s_semester');
        try:
            existing_student= users.objects.filter(v_email=s_email, v_password=s_password)
            if not existing_student:
                messages.error(request,"Email or Password is not matched")
                return JsonResponse({'status': 'error'})
            else:
              save_student=Students(u_name=s_name,u_email=s_email,u_password=s_password,u_gender=s_gender, s_section= s_section,s_semester=s_semester)
              save_student.save();
              request.session['user_ids'] =save_student.id
              messages.success(request,'Registered Successfully')
              return JsonResponse({'status': 'success'})
        except users.DoesNotExist:
            messages.error(request, "Email does not exist")
            print("Email does not exist")
            return redirect('/')
    return render(request, 'Home/Home.html')

from django.contrib.sessions.backends.db import SessionStore

def login(request):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            
        try:
            registered_admin = Admin.objects.get(u_email=email, u_password=password)
            # messages.success(request, "Success")
            request.session['user_id'] = registered_admin.u_email
            request.session['user_role'] = 'Admin'
            request.session.save()
            return redirect('/admin_dashboard.html')
        except Admin.DoesNotExist:
            pass

        try:
            registered_faculty = Faculty.objects.get(u_email=email, u_password=password)
            #messages.success(request, "Login Successfully")
            request.session['user_idf'] = registered_faculty.u_email
            request.session.save()
            return redirect('/MainFacultyPage.html')
        except Faculty.DoesNotExist:
            pass

        try:
            registered_student = Students.objects.get(u_email=email, u_password=password)
            #messages.success(request, "Login Successfully")
            request.session['user_ids'] = registered_student.u_email
            request.session.save()
            return redirect('/StudentEditProfile.html')
        except Students.DoesNotExist:
            pass

        # If none of the objects are found, return an error message
        messages.error(request, "Wrong email or password")
        print("Wrong email or password")
        return redirect('/')

    
    # return render(request, 'Home.html')


# Admin Views
def admin_dashboard(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    faculty=Faculty.objects.all()
    students=Students.objects.all()
    return render(request,'Admin/admin_dashboard.html',{'facultycount':Faculty.objects.count(),'studentscount':Students.objects.count(),'user':user,'faculty':faculty,'students':students})
def room(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    rooms=Rooms.objects.all()
    return render(request,'Admin/rooms.html',{'user':user,'rooms':rooms})
def courses(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    faculty=Faculty.objects.all()
    courses=Courses.objects.all()
    return render(request,'Admin/courses.html',{'user':user,'courses':courses,'faculty':faculty})
def sections(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    sections=Sections.objects.all()
    courses=Courses.objects.all()
    return render(request,'Admin/sections.html',{'user':user,'courses':courses,'sections':sections})
def semesters(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    semesters=Semesters.objects.all()
    sections=Sections.objects.all()
    return render(request,'Admin/semesters.html',{'user':user,'semesters':semesters,'sections':sections})
def faculty(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    faculty=Faculty.objects.all()
    courses=Courses.objects.all()
    preference_timer = FreferenceEnable.objects.get(id=1)
    startDatetime=preference_timer.startDatetime
    endDatetime=preference_timer.endDatetime
    return render(request,'Admin/faculty.html',{'user':user,'faculty':faculty,'courses':courses,'endDatetime':endDatetime,'startDatetime':startDatetime})
def students(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    students=Students.objects.all()
    return render(request,'Admin/students.html',{'user':user,'students':students})
def generate_timetable(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    faculty=Faculty.objects.all()
    courses=Courses.objects.all()
    return render(request,'Admin/generate_timetable.html',{'user':user,'courses':courses,'faculty':faculty})
def viewTimetable(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    approve_timer = FreferenceEnable.objects.filter(id=2).values().first()
    rooms= Rooms.objects.all()
    classes = Classes.objects.prefetch_related('class_semester','meeting_time', 'course', 'instructor', 'room', 'section').all()
    meetings = Meetings.objects.all()
    matching_data = []
    non_matching_data = []
    room_list = list(rooms)

    if classes and meetings:
        for meeting in meetings:
            if classes.filter(meeting_time__time=meeting.time, meeting_time__day=meeting.day).exists():
                matching_time_day = classes.filter(meeting_time__time=meeting.time, meeting_time__day=meeting.day)
                for matching_object in matching_time_day:
                    found_matching_room = False
                    for r in rooms:
                        found_matching_room = False  # Initialize the flag for each room iteration

                        for matching_object in matching_time_day:
                            if matching_object.room.r_name == r.r_name:
                                new_data1 = {
                                    'room': r.r_name,
                                    'time': matching_object.meeting_time.time,
                                    'day': matching_object.meeting_time.day,
                                    'Instructor': matching_object.instructor.u_name,
                                    'course':matching_object.course.c_name,
                                    }
                            # Check if the new_data already exists in non_matching_data
                                if new_data1 not in matching_data:
                                    matching_data.append(new_data1)
                                found_matching_room = True
                                break  # Exit the inner loop after appending the data

                        if not found_matching_room:
                            new_data = {
                                'room': r.r_name,
                                'time': matching_object.meeting_time.time,
                                'day': matching_object.meeting_time.day,
                                'course':matching_object.course.c_name
                            }
                            for matching_object in matching_time_day:
                                if matching_object.meeting_time.day== new_data['day'] and matching_object.meeting_time.time == new_data['time']:
                                    new_data['Instructor'] = matching_object.instructor.u_name
                                    new_data['semester'] = matching_object.class_semester.semester_no
                                    new_data['section'] = matching_object.section.section_name
                                else:
                                    new_data['Instructor'] = "ok"
                                    new_data['semester'] = "ok"
                                    new_data['section'] = "ok"
                            if new_data not in non_matching_data:

                                non_matching_data.append(new_data)

        # # Print matching data
        # print("Matching Data:")
        # for data in matching_data:
        #     print(data)

        # print("Non-Matching Data:")
        # for data in non_matching_data:
        #     print(data)

    if approve_timer:
       start_datetime = approve_timer['startDatetime']
       end_datetime = approve_timer['endDatetime']
       print(start_datetime, end_datetime)
       print("yes")
    else:
        print("no")
    Time= Help.objects.all()
    length = len(Time)
    print(length)
    length1=length/3
    length2=length1*2 
    length1=int(math.ceil(length1))
    length2=int(math.ceil(length2))
    
    length3=length1+1
    length5=length+1
    length4=length-length2

    
    droplist_semester = Semesters.objects.values('semester_no').distinct()
    droplist_section = Sections.objects.all()
    search_section = request.session.get('search_section')
    search_semester = request.session.get('search_semester')
    if search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester, sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif search_section and not search_semester:
        semester = Semesters.objects.filter(sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif not search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester).prefetch_related('sem_section').all()
    else:
        semester = Semesters.objects.prefetch_related('sem_section').all()
    
    section = Sections.objects.all()
    courses= Courses.objects.all()
    faculty=Faculty.objects.all()
    context = {
        'user': user,
        'classes': classes,
        'meetings': meetings,
        'Time': Time,
        'length':length,
        'length1':length1, 
        'length2':length2,
        'length3':length3,
        'length4':length4,
        'semester': semester,
        'droplist_section': droplist_section,
        'droplist_semester': droplist_semester,
        'search_section': search_section,
        'search_semester': search_semester,
        'start_datetime':start_datetime,
        'start_datetime':start_datetime,
        'end_datetime':end_datetime,
        'courses':courses,
        'faculty':faculty,
        'room':room,
        'non_matching_data':non_matching_data
        
        # 'non_matching_data':non_matching_data
    }
    return render(request,'Admin/viewTimetable.html',context)

def Replace_lecture_Slot(request):
    course_select = request.POST.get('course_select')
    instructor = request.POST.get('instructor')
    course = request.POST.get('course')
    day = request.POST.get('day')
    time = request.POST.get('time')
    room = request.POST.get('room')

    course_select1 = request.POST.get('course_select1')
    instructor1 = request.POST.get('instructor1')
    course1 = request.POST.get('course1')
    day1 = request.POST.get('day1')
    time1 = request.POST.get('time1')
    room1 = request.POST.get('room1')
    section = request.POST.get('section')
    semester = request.POST.get('semester')

    slot_day=request.POST.get('slot_day') 
    slot_time=request.POST.get('slot_time') 
    slot_room=request.POST.get('slot_room') 
    classes1 = Classes.objects.prefetch_related('class_semester', 'meeting_time', 'course', 'instructor', 'room', 'section').filter(
    instructor__u_name=instructor1,
    class_semester__semester_no=day1,
    course__c_code=course_select1,
    course__c_name=course1,
    section__section_name=time1,
    ).first()
    classes2 = Classes.objects.prefetch_related('class_semester', 'meeting_time', 'course', 'instructor', 'room', 'section').filter(
    instructor__u_name=instructor,
    meeting_time__time=time,
    course__c_code=course_select,
    meeting_time__day=day,
    ).first()
    if request.POST.get('option') == 'remove':
        if classes2:
            classes2.delete()
            messages.success(request, 'Your lecture is succesfully Remove From Timetable')
            return JsonResponse({'status': 'success'})
        else:
            error_message = "Data Is not Complete"
            return JsonResponse({'error_message': error_message})
    elif request.POST.get('option') == 'swap':
        if request.POST.get('agreenoyes') == 'lecture':
            if classes1 and classes2:
                            temp_meeting_time = classes1.meeting_time
                            classes1.meeting_time = classes2.meeting_time
                            classes2.meeting_time = temp_meeting_time

                            temp_room = classes1.room
                            classes1.room = classes2.room
                            classes2.room = temp_room

                            classes1.save()
                            classes2.save()

                            messages.success(request, 'Your lecture is succesfully Swap With Lecrure')
                            return JsonResponse({'status': 'success'})
            else:
                error_message = "Select the correct imformation according code"
                return JsonResponse({'error_message': error_message})
        

        
        elif request.POST.get('agreenoyes') == 'in_free_slot':
                        meeting_time_swap = Meetings.objects.filter(time=slot_time, day=slot_day).first()
                        room_swap = Rooms.objects.filter(r_name=slot_room).first()
                        course_swap = Courses.objects.filter(c_name=course).first()
                        semester_swap = Semesters.objects.filter(semester_no=classes2.class_semester.semester_no).first()
                        section_swap = Sections.objects.filter(section_name=classes2.section.section_name).first()
                        instructor_swap = Faculty.objects.filter(u_name=instructor).first()
                        # print("....good............", section_swap,semester_swap,course_swap,room_swap,slot_room)
                        if meeting_time_swap and room_swap and course_swap and semester_swap and section_swap and instructor_swap:
                            classes3 = Classes(
                                meeting_time=meeting_time_swap,
                                room=room_swap,
                                class_semester=semester_swap,
                                section=section_swap,
                                course=course_swap,
                                instructor=instructor_swap,   
                            )
                        else:
                            error_message="choose another room"
                            return JsonResponse({'error_message': error_message})

                        if classes3:
                            print(classes3)
                            classes3.save()
                            classes2.delete()
                            messages.success(request, 'Your lecture is succesfully Swap With Free Slot')
                            return JsonResponse({'status': 'success'})

                        else:
                            error_message="Something wrong! check your given data. Data is not complete"
                            return JsonResponse({'error_message': error_message})
                    
        else:
            error_message = "Data is Not Complete"
            return JsonResponse({'error_message': error_message})
    elif request.POST.get('option') == 'Add':
            instructor_add=request.POST.get('instructor_add') 
            section_add=request.POST.get('section_add') 
            course_add=request.POST.get('course_add') 
            semester_add=request.POST.get('semester_add') 
            classes4 = Classes.objects.prefetch_related('class_semester', 'meeting_time', 'course', 'instructor', 'room', 'section').filter(
            instructor__u_name=instructor_add,
            course__c_code=course_add,
            class_semester__semester_no=semester_add,
            section__section_name=section_add
            )
           
            if classes4:
                error_message = "That Lecture is Already exist "
                return JsonResponse({'error_message': error_message})
            else:
                if not course_add or not semester_add or not section_add or not instructor_add:
                    error_message = "Given Data is Not complete"
                    return JsonResponse({'error_message': error_message})

                else:
                    meeting_time_swap = Meetings.objects.filter(time=slot_time, day=slot_day).first()
                    room_swap = Rooms.objects.filter(r_name=slot_room).first()
                    course_swap = Courses.objects.filter(c_code=course_add).first()
                    semester_swap = Semesters.objects.filter(semester_no=semester_add).first()
                    section_swap = Sections.objects.filter(section_name=section_add).first()
                    instructor_swap = Faculty.objects.filter(u_name=instructor_add).first()
                    # print("....good............", section_swap,semester_swap,course_swap,room_swap,slot_room)
                    if meeting_time_swap and room_swap and course_swap and semester_swap and section_swap and instructor_swap:
                                    classes3 = Classes(
                                        meeting_time=meeting_time_swap,
                                        room=room_swap,
                                        class_semester=semester_swap,
                                        section=section_swap,
                                        course=course_swap,
                                        instructor=instructor_swap,   
                                    )
                    if classes3:
                        print(classes3)
                        classes3.save()
                        messages.success(request, 'Your lecture is succesfully Added')
                        return JsonResponse({'status': 'success'})
                    else:
                        error_message = "Given Data is Not complete "
                        return JsonResponse({'error_message': error_message})
                    

    elif request.POST.get('option') == 'Edit':
        
    
        course_edit=request.POST.get('course-select_edit') 
        instructor_Edit=request.POST.get('instructor_Edit') 
        print("hghgmjhgyytmy",course_edit,semester,section,instructor_Edit)
        classes5 = Classes.objects.prefetch_related('class_semester', 'meeting_time', 'course', 'instructor', 'room', 'section').filter(
            course__c_code=course_edit,
            class_semester__semester_no=semester,
            section__section_name=section
        )
        if classes5:
            instructor_swap = Faculty.objects.filter(u_name=instructor_Edit).first()
            for class_instance in classes5:  # Print the class instance for debugging purposes
                class_instance.instructor = instructor_swap
                class_instance.save()
                messages.success(request, 'Instructor is successfully change')
                return JsonResponse({'status': 'success'})
        else:
                error_message = "Somthing Wrong Check the given Data"
                return JsonResponse({'error_message': error_message})
    else:
        error_message = "Select an Option"
        return JsonResponse({'error_message': error_message})

def editProfile(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    courses=Courses.objects.all()
    context = {
        'user': user,
        'courses':courses
    }
    return render(request, 'Admin/editProfile.html', context)


def a_saveeditfrofile(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    if request.method == 'POST':
        # Update the user's information based on the form data
        user.u_name = request.POST.get('name')
        user.u_email = request.POST.get('email')
        user.u_contactNo = request.POST.get('contact_no')
        user.u_gender = request.POST.get('gender')
        user.u_department = request.POST.get('department')
        user.u_city = request.POST.get('a_city')
        if request.FILES.get('avatar'):
            user.u_profile_pic = request.FILES['avatar']
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return JsonResponse({'status': 'success'})

def check_approval_status(request):
    user_id = request.session.get('user_id')
    user = Admin.objects.get(u_email=user_id)
    faculty=Faculty.objects.all()
    return render(request,'Admin/check_approval_status.html',{'user': user,'faculty':faculty})

def add_room(request):
    if request.method=="POST":
        room_name=request.POST.get('r_name');
        room_type=request.POST.get('r_type');
        room_capacity=request.POST.get('r_capacity');
        room_department=request.POST.get('r_department');
        save_room=Rooms(r_name=room_name,r_type=room_type,r_capacity=room_capacity,r_department=room_department)
        save_room.save();
        rooms=Rooms.objects.all()
    return redirect('/rooms.html',{'room':rooms})

def del_room(request, id):
  room =Rooms.objects.get(id=id)
  room.delete()
  return redirect('/rooms.html')


def edit_room(request,id):
    if request.method=="POST":
        room_name=request.POST.get('r_name');
        room_type=request.POST.get('r_type');
        room_capacity=request.POST.get('r_capacity');
        room_department=request.POST.get('r_department');
        save_room=Rooms(id=id,r_name=room_name,r_type=room_type,r_capacity=room_capacity,r_department=room_department)
        save_room.save();
    return redirect('/rooms.html',)




def add_course(request):
    if request.method=="POST":
        course_name=request.POST.get('c_name');
        course_code=request.POST.get('c_code');
        course_semester=request.POST.get('c_semester');
        course_section=request.POST.get('c_section');
        course_type=request.POST.get('c_type');
        max_numb_students=request.POST.get('max_numb_students')
        course_faculty_names = request.POST.getlist('c_instructers')
        # Create and save a new Faculty instance
        new_course = Courses.objects.create(c_name=course_name,
                                              c_code=course_code,
                                              max_numb_students=max_numb_students,
                                              c_semester=course_semester,
                                              c_section=course_section,
                                              c_type=course_type)
        
        # Add Faculty to the new Course instance
        for faculty_name in course_faculty_names:
            faculty = Faculty.objects.get(u_name=faculty_name)
            new_course.instructors.add(faculty)
    faculty=Faculty.objects.all();
    courses=Courses.objects.all();
    return redirect('/courses.html',{courses:'courses',faculty:'faculty'})

def del_course(request, id):
  course =Courses.objects.get(id=id)
  course.delete()
  return redirect('/courses.html')

from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404

def edit_course(request, id):
    if request.method == "POST":
        course_name = request.POST.get('c_name')
        course_code = request.POST.get('c_code')
        course_semester = request.POST.get('c_semester')
        course_section = request.POST.get('c_section')
        course_type = request.POST.get('c_type')
        max_numb_students = request.POST.get('max_numb_students')
        course_faculty_names = request.POST.getlist('c_instructers')
        
        course = get_object_or_404(Courses, id=id)
        
        # Check if the provided code and section are already used by another course
        if course.c_code != course_code or course.c_section != course_section:
            # If the code or section is changed, check for uniqueness
            existing_course = Courses.objects.filter(c_code=course_code, c_section=course_section).exclude(id=id)
            if existing_course.exists():
                # A course with the same code and section already exists
                # Delete the existing course
                existing_course.delete()
        
        course.c_name = course_name
        course.c_code = course_code
        course.c_semester = course_semester
        course.c_section = course_section
        course.c_type = course_type
        course.max_numb_students = max_numb_students
        
        # Clear the existing faculty assignments and add the updated ones
        course.instructors.clear()
        for faculty_name in course_faculty_names:
            faculty = Faculty.objects.get(u_name=faculty_name)
            course.instructors.add(faculty)
        
        course.save()
    
    return redirect('/courses.html')


def add_section(request):
    if request.method=='POST':
        section_name=request.POST.get('section_name')
        section_course_names = request.POST.getlist('section_courses')
        # Create and save a new Faculty instance
        new_section = Sections.objects.create(section_name=section_name,)
        
        # Add courses to the new faculty instance
        for course_name in section_course_names:
            try:
                courses = Courses.objects.filter(c_name=course_name)
            except Courses.DoesNotExist:
                # Handle the case when the course doesn't exist
                # This can be logging an error, displaying a message, or taking any other appropriate action
                pass
            else:
                for course in courses:
                    new_section.courses.add(course)
    sections=Sections.objects.all();
    return redirect('/sections.html',{'sections': sections})

def edit_section(request,id):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        section_course_names = request.POST.getlist('section_courses')
        
        # Retrieve the existing section
        section = Sections.objects.get(id=id)
        
        # Update the properties of the section
        section.section_name = section_name
        
        # Remove existing courses from the section
        section.courses.clear()
        
        # Add courses to the section
        for course_name in section_course_names:
            course = Courses.objects.get(c_name=course_name)
            section.courses.add(course)
        
        # Save the changes to the section
        section.save()
    
    sections = Sections.objects.all()
    return redirect('/sections.html', {'sections': sections})

def del_section(request,id):
    section =Sections.objects.get(id=id)
    section.delete()
    return redirect('/sections.html',{'section':section})
def add_semester(request):
    if request.method == 'POST':
        # Get the form data from the request
        semester_no = request.POST.get('semester_no')
        num_class_in_week = request.POST.get('num_class_in_week')
        section_names = request.POST.getlist('sections')
        
        # Create a new Semester object and set its fields
        semester = Semesters.objects.create(
        semester_no=semester_no,
        num_class_in_week=num_class_in_week,
        sem_section=Sections.objects.get(section_name=section_names[0]))
        

        # Save the Semester object to the database
        semester.save()

        # Redirect to the list of Semesters
        semesters = Semesters.objects.all()
        return redirect('semesters.html',{'semesters': semesters})
def edit_semester(request, id):
    if request.method == "POST":
        semester_no = request.POST.get('semester_no')
        section_name = request.POST.get('section')

        # Get the Sections instance based on the section_name
        section = Sections.objects.get(section_name=section_name)

        num_class_in_week = request.POST.get('num_class_in_week')

        # Retrieve the existing Semesters instance
        semester = Semesters.objects.get(pk=id)

        # Update the fields of the Semesters instance
        semester.semester_no = semester_no
        semester.sem_section = section
        semester.num_class_in_week = num_class_in_week

        semester.save()

    return redirect('/semesters.html', {'semesters': semesters})
def del_semester(request,id):
    semester =Semesters.objects.get(id=id)
    semester.delete()
    return redirect('/semesters.html',{'semesters':semesters})


def add_faculty(request):
    if request.method == "POST":
        faculty_name = request.POST.get('f_name')
        faculty_email = request.POST.get('f_email')
        faculty_password = request.POST.get('f_password')
        faculty_gender = request.POST.get('f_gender')
        faculty_department = request.POST.get('f_department')
        faculty_course_names = request.POST.getlist('f_courses')
        # Create and save a new Faculty instance
        try:
            existing_faculty= users.objects.filter(v_email=faculty_email, v_password=faculty_password)
            if  not existing_faculty:
                messages.error(request,"Email or Password is not matched")
            else:
               new_faculty = Faculty.objects.create(u_name=faculty_name,
                                              u_email=faculty_email,
                                              u_password=faculty_password,
                                              u_gender=faculty_gender,
                                              u_department=faculty_department)
               for course_name in faculty_course_names:
                  course = Courses.objects.get(c_name=course_name)
                  new_faculty.f_courses.add(course)
               faculty=Faculty.objects.all();
               messages.success(request,"Record inserted sucessfully")
               return redirect('/faculty.html',{'faculty':faculty})
        except users.DoesNotExist:
            messages.error(request, "Email does not exist")
            print("Email does not exist")
        return redirect('/faculty.html')

def del_faculty(request, id):
  faculty =Faculty.objects.get(id=id)
  faculty.delete()
  return redirect('/faculty.html')

def edit_faculty(request, id):
    if request.method == "POST":
        faculty_name = request.POST.get('f_name')
        faculty_email = request.POST.get('f_email')
        faculty_gender = request.POST.get('f_gender')
        faculty_department = request.POST.get('f_department')
        faculty_course_names = request.POST.getlist('f_courses')
        
        # Retrieve the faculty instance
        faculty = Faculty.objects.get(id=id)
        
        # Update the faculty instance with the new data
        faculty.u_name = faculty_name
        faculty.u_email = faculty_email
        faculty.u_gender = faculty_gender
        faculty.u_department = faculty_department
        
        # Clear the existing courses and add the updated courses to the faculty instance
        faculty.f_courses.clear()
        for course_name in faculty_course_names:
            course = Courses.objects.get(c_name=course_name)
            faculty.f_courses.add(course)
        
        faculty.save()
        return redirect('/faculty.html')
    else:
        faculty = Faculty.objects.get(id=id)
        courses = Courses.objects.all()
        context = {
            'faculty': faculty,
            'courses': courses
        }
        return render(request, 'edit_faculty.html', context)

def mail_faculty(request, id):
    if request.method == "POST":
        faculty_email = request.POST.get('f_email')
        faculty_password = request.POST.get('s_password')
        from_email = settings.EMAIL_HOST_USER
        subject = 'Register By Admin'
        recipient_list = faculty_email

        # Build the description with line breaks using <br> tags
        description = 'Dear Madam,\n'
        description += 'I hope this message finds you well. Please find below your login details for your ATG account:\n'
        description += 'Your email ID: ' + faculty_email + '\n'
        description += 'Your password: ' + faculty_password + '\n'
        description += 'To access your account, please click on the following link:\n'
        description += 'http://127.0.0.1:8000/''\n'
        description += 'Best regards,'

        if send_mail(subject, description, from_email, [recipient_list], fail_silently=True):
            messages.success(request, "Email successfully sent.")

    return redirect('/faculty.html')

def mail_student(request, id):
    if request.method == "POST":
        student_email = request.POST.get('f_email')
        student_password = request.POST.get('s_password')
        from_email = settings.EMAIL_HOST_USER
        subject = 'Register By Admin'
        recipient_list = student_email

        # Build the description with line breaks using <br> tags
        description = 'Dear Student,\n'
        description += 'I hope this message finds you well. Please find below your login details for your ATG account:\n'
        description += 'Your email ID: ' + student_email + '\n'
        description += 'Your password: ' + student_password + '\n'
        description += 'To access your account, please click on the following link:\n'
        description += 'http://127.0.0.1:8000/''\n'
        description += 'Best regards,'

        if send_mail(subject, description, from_email, [recipient_list], fail_silently=True):
            messages.success(request, "Email successfully sent.")

    return redirect('/students.html')

def response_mail_faculty(request, id):
    if request.method == "POST":
        faculty_email = request.POST.get('f_email')
        faculty_response = request.POST.get('response')
        from_email = settings.EMAIL_HOST_USER
        subject = 'Register By Admin'
        recipient_list = faculty_email

        # Build the description with line breaks using <br> tags
        description = 'Greetings,\n'
        description += 'I hope this email finds you in good health.\n'
        description += 'Here is an update on the approval status you provided:\n'
        description += 'Approval Status Response:\n'
        description += '"' + faculty_response + '"\n'
        description +='Best regards, \n '
        if send_mail(subject, description, from_email, [recipient_list], fail_silently=True):
            messages.success(request, "Email successfully sent.")

    return redirect('/check_approval_status.html')
def add_student(request):
    if request.method=='POST':
        student_name=request.POST.get('s_name');
        student_email=request.POST.get('s_email');
        student_password=request.POST.get('s_password');
        student_gender=request.POST.get('s_gender');
        student_session=request.POST.get('s_session');
        student_semester=request.POST.get('s_semester');
        student_department=request.POST.get('s_department');
        try:
            existing_student= users.objects.filter(v_email=student_email, v_password=student_password)
            if  not existing_student:
                messages.error(request,"Email or Password is not matched")
            else:
              save_student=Students(u_name=student_name, u_email=student_email,u_password=student_password, u_gender=student_gender,u_department=student_department, s_session=student_session, s_semester=student_semester);
              save_student.save();
              students=Students.objects.all()
            return redirect('/students.html',{'students':students})
        except:
             messages.error(request, "Email does not exist")
             print("Email does not exist")
             return redirect('/students.html')
       
    

def del_student(request, id):
  student =Students.objects.get(id=id)
  student.delete()
  return redirect('/students.html')

def edit_student(request, id):
    if request.method=='POST':
        student_name=request.POST.get('s_name');
        student_email=request.POST.get('s_email');
        student_gender=request.POST.get('s_gender');
        student_session=request.POST.get('s_session');
        student_semester=request.POST.get('s_semester');
        student_department=request.POST.get('s_department');
        save_student=Students(id=id,u_name=student_name, u_email=student_email, u_gender=student_gender, s_session=student_session, s_semester=student_semester,u_department=student_department);
        save_student.save();
    return redirect('/students.html',)
def save_details(request):
    if request.method=='POST':
        department=request.POST.get('department');
        section=request.POST.get('section');
        shift=request.POST.get('shift');
        startTime=request.POST.get('startTime');
        offTime=request.POST.get('offTime');
        slotTime=request.POST.get('duration');
        # firstWorkingDay=request.POST.get('startDay');
        # lastWorkingDay=request.POST.get('lastDay');
        save_detail=Table(Department=department, Section=section, Shift=shift, StartTime=startTime,OffTime=offTime,SlotTime=slotTime);
        save_detail.save();
        table_instance = Table.objects.filter(Department=department, Section=section, Shift=shift, StartTime=startTime, OffTime=offTime, SlotTime=slotTime).last()
        Meetings.generate_meetings(table_instance)
        Help.generate_slottime(table_instance)
    return redirect('/generate_timetable.html')

def generate(request):
    if request.method=='POST':
       
       return redirect('/generate_timetable.html') 
    
def allocation(request):
    if request.method == 'POST':
        # Get the form data from the request
        course = request.POST.get('course')
        teacher=request.POST.get('teacher')
        
        # Create a new Semester object and set its fields
        course_faculty = CourseFaculty.objects.create(
        Subject=Courses.objects.get(c_name=course),
        Teacher=Faculty.objects.get(u_name=teacher))  

        course_faculty.save()
        return redirect('/generate_timetable.html')

# Faculty Views

def FacultyEditProfile(request):
    user_id = request.session.get('user_idf')
    user = Faculty.objects.get(u_email=user_id)
    courses=Courses.objects.all()
    num_courses = len(courses)
    selected_courses =user.f_courses
    print(selected_courses)
    certificates = user.f_certificates.all()
    section= Sections.objects.all()
    selected_section=user.u_department
    context = {
        'user': user,
        'certificates': certificates,
        'courses':courses,
        'section':section,
        'selected_section':selected_section,
        'selected_courses': selected_courses,
        'num_courses':num_courses

    }
    return render(request, 'Faculty/FacultyEditProfile.html', context)



    
def f_saveeditfrofile(request):
    user_id = request.session.get('user_idf')
    faculty_obj = Faculty.objects.get(u_email=user_id)
  
    if request.method == 'POST':
        ### Get list of Certificates from html file
        uploaded_files = request.FILES.getlist('certifi')
        uploaded_certificates = []

        ### Loop through each file and create a Certificate instance for it
        for uploaded_file in uploaded_files:
            certificate = Certificate()
            certificate.name = uploaded_file.name
            certificate.file.save(uploaded_file.name, uploaded_file)
            certificate.save()
            uploaded_certificates.append(certificate)
        
        

        f_pic = request.FILES.get('f_pic') 
        f_name = request.POST.get('f_name')
        f_email = request.POST.get('f_email')
        f_c_number = request.POST.get('f_c_number')
        f_gender = request.POST.get('f_gender')
        f_department = request.POST.get('f_department')
        f_course = request.POST.getlist('f_course')
        f_city = request.POST.get('f_city')
        # Update its attributes
        faculty_obj.u_name = f_name          
        faculty_obj.u_contactNo = f_c_number
        faculty_obj.u_city = f_city
        faculty_obj.u_email = f_email
        faculty_obj.u_department = f_department
        faculty_obj.u_gender = f_gender
        faculty_obj.f_course = f_course
        ## Inserting Certificates in the database using many-to-many relationship
        for certificate in uploaded_certificates:
            faculty_obj.f_certificates.add(certificate)

        # Check if a new picture has been uploaded and update the f_pic field
        if f_pic:
            faculty_obj.u_profile_pic = f_pic

        faculty_obj.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return JsonResponse({'status': 'success'})

def delete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    # delete file from server
    os.remove(certificate.file.path)
    # delete certificate from database
    certificate.delete()
    messages.success(request,'Certificate deleted successfully')
    return redirect('certificates')

def prefrencefunction(request):   
    preference_start_time = request.POST.get('preference_start_time') 
    preference_start_time = datetime.strptime(preference_start_time, "%Y-%m-%dT%H:%M")

    preference_end_time = request.POST.get('preference_end_time') 
    preference_end_time = datetime.strptime(preference_end_time, "%Y-%m-%dT%H:%M")
    
    now = preference_start_time
    future_datetime = preference_end_time
    data_put=FreferenceEnable(id=1,startDatetime=now,endDatetime=future_datetime)
    data_put.save()

    from_email=settings.EMAIL_HOST_USER
    subject='Timetable Approval Request'
    description='Dear Madam,\n'
    description +='I hope this message finds you well. We kindly request your approval for the proposed timetable.\n'
    description +='To provide your approval status, please log in to our website using the following link: http://127.0.0.1:8000/\n'
    description +='Thank you for your prompt attention to this matter.\n'
    description +='Best regards,\n'
    faculty_emails = Faculty.objects.values_list('u_email', flat=True)
    recipent_list = list(faculty_emails)
    if send_mail(subject, description, from_email, recipent_list, fail_silently=True):
            messages.success(request, "Email sent to all Faculty Members requesting their preferences.The preference fields are now accessible.")
    return JsonResponse({'status': 'success'})

def referencefunt(request):
    approve_start_time = request.POST.get('approve_start_time') 
    approve_start_time = datetime.strptime(approve_start_time, "%Y-%m-%dT%H:%M")

    approve_end_time = request.POST.get('approve_end_time') 
    approve_end_time = datetime.strptime(approve_end_time, "%Y-%m-%dT%H:%M")
    
    now = approve_start_time
    future_datetime = approve_end_time
    data_put=FreferenceEnable(id=2,startDatetime=now,endDatetime=future_datetime)
    data_put.save()

    from_email=settings.EMAIL_HOST_USER
    subject='Timetable Approval Request'
    description='Dear Madam,\n'
    description +='I hope this message finds you well. We kindly request your approval for the proposed timetable.\n'
    description +='To provide your approval status, please log in to our website using the following link: http://127.0.0.1:8000/\n'
    description +='Thank you for your prompt attention to this matter.\n'
    description +='Best regards,\n'
    faculty_emails = Faculty.objects.values_list('u_email', flat=True)
    recipent_list = list(faculty_emails)
    if send_mail(subject, description, from_email, recipent_list, fail_silently=True):
        messages.success(request, "Email sent to all Faculty Members requesting Approval Status.The Approval Status fields are now accessible.")
    return JsonResponse({'status': 'success'})
def MainFacultyPage(request):
    user_id = request.session.get('user_idf')
    user = Faculty.objects.get(u_email=user_id)
    meetings=Meetings.objects.all()
    Time= Help.objects.all()
    length = len(Time)
    print(length)
    length1=length/3
    length2=length1*2 
    length1=int(math.ceil(length1))
    length2=int(math.ceil(length2))
    
    length3=length1+1
    length5=length+1
    length4=length-length2
    classes = Classes.objects.prefetch_related( 'meeting_time', 'course','instructor','room','section','class_semester').all()
    semester= Semesters.objects.all()
    try:
     
        karachi_timezone = pytz.timezone('Asia/Karachi')
        data = FreferenceEnable.objects.order_by('id').last()
        start_datetime_str = data.startDatetime.strftime('%Y-%m-%d %H:%M')
        start_datetime_obj = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        start_datetime_obj = karachi_timezone.localize(start_datetime_obj)
        start_datetime_str = start_datetime_obj.strftime('%Y-%m-%d %H:%M')

        end_datetime_str = data.endDatetime.strftime('%Y-%m-%d %H:%M')
        end_datetime_obj = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        end_datetime_obj = karachi_timezone.localize(end_datetime_obj)
        end_datetime_str = end_datetime_obj.strftime('%Y-%m-%d %H:%M')

        print(start_datetime_str,end_datetime_str)
        context = {
            'start_datetime': start_datetime_str,
            'end_datetime': end_datetime_str,
            'user':user,
            'classes': classes,
            'meetings':meetings,
             'Time': Time,
            'length':length,
            'length1':length1, 
            'length2':length2,
            'length3':length3,
            'length4':length4,
            'semester':semester
            }
    except:
        context = {'data': ''}
        print(context)
    if not any(message.level == messages.SUCCESS for message in messages.get_messages(request)):
        messages.success(request, '')
    return render(request,'Faculty/MainFacultyPage.html',context)

def FacultyGiveApproval(request):
    user_id = request.session.get('user_id')
    user = Faculty.objects.get(u_email=user_id)
    try:
      
        karachi_timezone = pytz.timezone('Asia/Karachi')
        data = FreferenceEnable.objects.get(id=2)
        start_datetime_str = data.startDatetime.strftime('%Y-%m-%d %H:%M')
        start_datetime_obj = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        start_datetime_obj = karachi_timezone.localize(start_datetime_obj)
        start_datetime_str = start_datetime_obj.strftime('%Y-%m-%d %H:%M')

        end_datetime_str = data.endDatetime.strftime('%Y-%m-%d %H:%M')
        end_datetime_obj = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        end_datetime_obj = karachi_timezone.localize(end_datetime_obj)
        end_datetime_str = end_datetime_obj.strftime('%Y-%m-%d %H:%M')

        print(start_datetime_str,end_datetime_str)
        context = {'start_datetime': start_datetime_str, 'end_datetime': end_datetime_str,'user':user}

    except:
        context = {'data': ''}
        print(context)
    if not any(message.level == messages.SUCCESS for message in messages.get_messages(request)):
        messages.success(request, '')
    return render(request,'Faculty/FacultyGiveApproval.html',context)


def FacultyGivePrefernces(request):
    user_id = request.session.get('user_idf')
    user = Faculty.objects.get(u_email=user_id) 
    selected_courses =user.f_CoursePref
    selected_room =user.f_RoomPref
    print(selected_courses)
    courses=Courses.objects.all()
    room=Rooms.objects.all()

    try:
        karachi_timezone = pytz.timezone('Asia/Karachi')
        data = FreferenceEnable.objects.get(id=1)
        start_datetime_str = data.startDatetime.strftime('%Y-%m-%d %H:%M')
        start_datetime_obj = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        start_datetime_obj = karachi_timezone.localize(start_datetime_obj)
        start_datetime_str = start_datetime_obj.strftime('%Y-%m-%d %H:%M')

        end_datetime_str = data.endDatetime.strftime('%Y-%m-%d %H:%M')
        end_datetime_obj = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        end_datetime_obj = karachi_timezone.localize(end_datetime_obj)
        end_datetime_str = end_datetime_obj.strftime('%Y-%m-%d %H:%M')
        context = {
        'start_datetime': start_datetime_str, 
        'end_datetime': end_datetime_str,
        'user':user,
        'courses':courses,
        'selected_courses':selected_courses,
        'room':room,
        'selected_room':selected_room
        }
    except:
        context = {'data': ''}
        print(context) 
    return render(request,'Faculty/FacultyGivePrefernces.html',context)




def FacultyViewtimetable(request):
    user_id = request.session.get('user_idf')
    user = Faculty.objects.get(u_email=user_id)
    meetings = Meetings.objects.all()
    Time= Help.objects.all()
    length = len(Time)
    print(length)
    length1=length/3
    length2=length1*2 
    length1=int(math.ceil(length1))
    length2=int(math.ceil(length2))
    
    length3=length1+1
    length5=length+1
    length4=length-length2

    
    classes = Classes.objects.prefetch_related('meeting_time', 'course', 'instructor', 'room', 'section').all()
    droplist_semester = Semesters.objects.prefetch_related('sem_section').all()
    droplist_section = Sections.objects.all()
    search_section = request.session.get('search_section')
    search_semester = request.session.get('search_semester')
    if search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester, sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif search_section and not search_semester:
        semester = Semesters.objects.filter(sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif not search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester).prefetch_related('sem_section').all()
    else:
        semester = Semesters.objects.prefetch_related('sem_section').all()
    
    section = Sections.objects.all()
    context = {
        'user': user,
        'classes': classes,
        'meetings': meetings,
        'Time': Time,
        'length':length,
        'length1':length1, 
        'length2':length2,
        'length3':length3,
        'length4':length4,
        'semester': semester,
        'droplist_section': droplist_section,
        'droplist_semester': droplist_semester,
        'search_section': search_section,
        'search_semester': search_semester
    }

    if not any(message.level == messages.SUCCESS for message in messages.get_messages(request)):
        messages.success(request, '')
    return render(request, 'Faculty/FacultyViewtimetable.html', context)






def f_giveaproval(request):
    if request.method=='POST':
        user_id = request.session.get('user_idf')
        user = Faculty.objects.get(u_email=user_id)
        f_approve=request.POST.get('agreenoyes')
        f_reason=request.POST.get('reasonforno')
        user.f_ApprovalStatus=f_approve
        user.f_Comment=f_reason
        user.save()
    try:
       
       
        
        karachi_timezone = pytz.timezone('Asia/Karachi')
        data = FreferenceEnable.objects.order_by('id').last()
        start_datetime_str = data.startDatetime.strftime('%Y-%m-%d %H:%M')
        start_datetime_obj = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        start_datetime_obj = karachi_timezone.localize(start_datetime_obj)
        start_datetime_str = start_datetime_obj.strftime('%Y-%m-%d %H:%M')

        end_datetime_str = data.endDatetime.strftime('%Y-%m-%d %H:%M')
        end_datetime_obj = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        end_datetime_obj = karachi_timezone.localize(end_datetime_obj)
        end_datetime_str = end_datetime_obj.strftime('%Y-%m-%d %H:%M')

        context = {'start_datetime': start_datetime_str, 'end_datetime': end_datetime_str,'user':user}

    except:
        context = {'data': ''}
     
        print(context)
    messages.success(request, 'Your Approval for TimeTable is Saved.')
    return JsonResponse({'status': 'success'})


def f_g_prefrences(request):

    if request.method=='POST':
        user_id = request.session.get('user_idf')
        user = Faculty.objects.get(u_email=user_id)
        f_r1=request.POST.get('proom1')
        f_c1=request.POST.get('pcourse1')
        f_t1=request.POST.get('f_t1') 
        f_t2=request.POST.get('f_t2')
        if not f_t1:
            f_t1 = '08:00:00'
        if not f_t2:
            f_t2 = '16:00:00'
        user.f_RoomPref=f_r1
        user.f_CoursePref=f_c1
        user.f_startTimePref=f_t1
        user.f_endTimePref=f_t2
        user.save()
      
    try:
   
        karachi_timezone = pytz.timezone('Asia/Karachi')
        data = FreferenceEnable.objects.order_by('id').last()
        start_datetime_str = data.startDatetime.strftime('%Y-%m-%d %H:%M')
        start_datetime_obj = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
        start_datetime_obj = karachi_timezone.localize(start_datetime_obj)
        start_datetime_str = start_datetime_obj.strftime('%Y-%m-%d %H:%M')

        end_datetime_str = data.endDatetime.strftime('%Y-%m-%d %H:%M')
        end_datetime_obj = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')
        end_datetime_obj = karachi_timezone.localize(end_datetime_obj)
        end_datetime_str = end_datetime_obj.strftime('%Y-%m-%d %H:%M')

        context = {'start_datetime': start_datetime_str, 'end_datetime': end_datetime_str,'user':user}

    except:
        context = {'data': ''}
        print(context)
    messages.success(request, 'Your Preferences are successfully save in Database.')
    return JsonResponse({'status': 'success'})

def search_timetable(request):
    if request.method == 'POST':
        search_section = request.POST.get('section')
        search_semester = request.POST.get('semester')
        request.session['search_section'] = search_section
        request.session['search_semester'] = search_semester
        request.session['skip_faculty_view'] = True
        # Perform the search using the selected values
        # You can query your database or perform any other necessary operations here
        
        # Render the search results or perform any other desired action
        return JsonResponse({'status': 'success'})
    
    # Handle GET requests or render the initial search form
    return render(request, 'Faculty/FacultyViewtimetable.html')

def fsavebtn(request):
    user_ida = request.session.get('user_ida')
    user = Admin.objects.get(u_email=user_ida)
    try:
        if request.method == 'POST':
            a_name = request.POST.get('a_name')
            a_cnumber = request.POST.get('a_cnumber')
            a_email = request.POST.get('a_email')
            a_pic = request.FILES.get('a_pic') 
            a_department = request.POST.get('a_department')
            a_gender = request.POST.get('a_gender')
            a_city = request.POST.get('a_city')
            user.u_name = a_name
            user.u_c_number = a_cnumber
            user.u_city = a_city
            user.u_email = a_email
            user.u_department = a_department
            user.u_gender = a_gender
            if a_pic:
                user.u_profile_pic = a_pic
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
    except:
        messages.success(request, 'Sorry, an error occurred while updating your profile.')
        
    return JsonResponse({'status': 'success'})
def ssavebtn(request):
    user_ids = request.session.get('user_ids')
    user = Students.objects.get(u_email=user_ids)
    try:
        if request.method=='POST':
            s_name=request.POST.get('s_name')
            s_department=request.POST.get('s_department')
            s_semester=request.POST.get('s_semester')
            s_section=request.POST.get('s_section')
            s_c_number=request.POST.get('s_c_number')
            s_email=request.POST.get('s_email')
            s_pic=request.FILES.get('s_pic') 
            s_gender=request.POST.get('s_gender')
            user.u_name = s_name
            user.u_email = s_email
            user.u_department = s_department
            user.s_section=s_section
            user.u_contactNo=s_c_number
            user.s_semester=s_semester
            user.u_gender = s_gender
            if s_pic:
                user.u_profile_pic = s_pic
            user.save()
            
            messages.success(request, 'Your profile has been updated successfully.')
    except:
        messages.success(request, 'sorry')
    return JsonResponse({'status': 'success'})


# Student Views
def StudentEditProfile(request):
        user_ids = request.session.get('user_ids')
        user = Students.objects.get(u_email=user_ids)
        semester= Semesters.objects.all()
        selected_semester = user.s_semester
        section= Sections.objects.all()
        selected_section=user.s_section
        print(selected_section)
        context = {
        'user': user,
        'semester': semester,
        'selected_semester': selected_semester,
        'section':section,
        'selected_section':selected_section
            }
        return render(request,'Student/StudentEditProfile.html',context)  

def sviewtimetable(request):
    user_ids = request.session['user_ids']
    user = Students.objects.get(u_email=user_ids)
    meetings=Meetings.objects.all()
    Time= Help.objects.all()
    length = len(Time)
    print(length)
    length1=length/3
    length2=length1*2 
    length1=int(math.ceil(length1))
    length2=int(math.ceil(length2))
    
    length3=length1+1
    length5=length+1
    length4=length-length2

    
    classes = Classes.objects.prefetch_related('meeting_time', 'course', 'instructor', 'room', 'section').all()
    droplist_semester = Semesters.objects.prefetch_related('sem_section').all()
    droplist_section = Sections.objects.all()
    search_section = request.session.get('search_section')
    search_semester = request.session.get('search_semester')
    if search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester, sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif search_section and not search_semester:
        semester = Semesters.objects.filter(sem_section__section_name=search_section).prefetch_related('sem_section').all()
    elif not search_section and search_semester:
        semester = Semesters.objects.filter(semester_no=search_semester).prefetch_related('sem_section').all()
    else:
        semester = Semesters.objects.prefetch_related('sem_section').all()
    
    section = Sections.objects.all()
    context = {
        'user': user,
        'classes': classes,
        'meetings': meetings,
        'Time': Time,
        'length':length,
        'length1':length1, 
        'length2':length2,
        'length3':length3,
        'length4':length4,
        'semester': semester,
        'droplist_section': droplist_section,
        'droplist_semester': droplist_semester,
        'search_section': search_section,
        'search_semester': search_semester
    }
    return render(request, 'Student/sviewtimetable.html', context)

#logout
def logout_view(request):
    logout(request)
    return render(request, 'Home/Home.html')

#Generate Timetable
   
class Data:
    def __init__(self):
        self._rooms = Rooms.objects.all()
        self._meetingTimes = Meetings.objects.all()
        self._instructors = Faculty.objects.all()
        self._courses = Courses.objects.all()
        self._sections = Sections.objects.all()
        self._semesters = Semesters.objects.all()
        self._courseFaculty=CourseFaculty.objects.all()

    def get_rooms(self): return self._rooms

    def get_instructors(self): return self._instructors

    def get_courses(self): return self._courses

    def get_sections(self): return self._sections

    def get_meetingTimes(self): return self._meetingTimes

    def get_semesters(self): return self._semesters

    def get_courseFaculty(self): return self._courseFaculty

# Timetable
class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, elitism):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.data = Data()
        self.rooms = self.data.get_rooms()
        self.instructors = self.data.get_instructors()
        self.courseFaculty = self.data.get_courseFaculty()
        self.courses = self.data.get_courses()
        self.sections = self.data.get_sections()
        self.semesters = self.data.get_semesters()
        self.meeting_times = self.data.get_meetingTimes()
        self.classes = []

        self.course_faculty_map = {}  # Store the allocated faculty for each course

        # Populate the course_faculty_map
        for course_faculty in self.courseFaculty:
            subject = course_faculty.Subject
            teacher = course_faculty.Teacher
            self.course_faculty_map[subject] = teacher

       # Generate random initial population
        for i in range(self.population_size):
            chromosome = self.generate_random_chromosome()
            self.classes.append(chromosome)

    def generate_random_chromosome(self):
        chromosome = []
        available_slots = set(self.meeting_times)  # Set of available meeting times

        for section in self.sections:
            filtered_semesters = [sem for sem in self.semesters if str(sem.sem_section) == str(section)]

            for semester in filtered_semesters:
                filtered_courses = [course for course in self.courses if str(course.c_semester) == str(semester) and str(course.c_section) == str(section)]

                for course in filtered_courses:
                    instructor = self.course_faculty_map.get(course, None)  # Get the allocated faculty for the course
                    if instructor is None:
                        continue  # Skip the course if no faculty is allocated
                    room = random.choice(self.rooms)

                    if not available_slots:
                        break  # No available meeting times left, exit the loop
                    meeting_time = random.choice(list(available_slots))  # Choose from available meeting times
                    available_slots.remove(meeting_time)  # Remove the selected meeting time from available slots
                    chromosome.append((room, instructor, course, section, semester, meeting_time))
        return chromosome

    def fitness(self, chromosome):
        # Evaluate fitness of a chromosome based on hard and soft constraints
        penalty = 0
        bonus = 0
        # Hard constraints
        room_set = set()
        instructor_set = set()
        section_set = set()
        semester_set = set()
        time_slot_set = set()  # New set to track assigned time slots
        for i in range(len(chromosome)):
            room, instructor, course, section, semester, meeting_time = chromosome[i]
            if instructor is None:
                penalty += 1
                continue

            if (
                room in room_set
                or instructor in instructor_set
                or section in section_set
                or semester in semester_set
            ):
                penalty += 1
            else:
                room_set.add(room)
                instructor_set.add(instructor)
                section_set.add(section)
                semester_set.add(semester)
                # student_set.add(course.student)
            # Check if the same section is scheduled in different semesters
            if section.section_name in [
                chromosome[j][3].section_name for j in range(len(chromosome)) if j != i
            ]:
                penalty += 1
            # Check for duplicate time slots
            if meeting_time in time_slot_set:
                penalty += 1
            else:
                time_slot_set.add(meeting_time)
        # Soft constraints
        for i in range(len(chromosome)):
            room, instructor, course, section, semester, meeting_time = chromosome[i]
            if instructor is None:
                continue

            if str(instructor.f_startTimePref) <= str(meeting_time.time) <= str(instructor.f_endTimePref):
                bonus += 1
            if room.r_name == instructor.f_RoomPref:
                bonus += 1
            if i > 0:
                prev_instructor = chromosome[i - 1][1]
                if instructor == prev_instructor:
                    penalty += 1
        return bonus - penalty

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create two children
        if random.random() < self.crossover_rate:
            # Choose a random crossover point
            crossover_point = random.randint(0, len(parent1)-1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2

    def mutate(self, chromosome):
        mutated_chromosome = []
        for i in range(len(chromosome)):
            room, instructor, course, section,semester, meeting_time = chromosome[i]
            if random.random() < self.mutation_rate:
                room = random.choice(self.rooms)
            if random.random() < self.mutation_rate:
                instructor = random.choice(self.instructors)
            if random.random() < self.mutation_rate:
                section = random.choice(self.sections)
            if random.random() < self.mutation_rate:
                semester = random.choice(self.semesters)
            if random.random() < self.mutation_rate:
                meeting_time = random.choice(self.meeting_times)
            mutated_chromosome.append((room, instructor, course, section,semester, meeting_time))
        return mutated_chromosome

    def select_parents(self):
        # Select two parents using roulette wheel selection
        fitnesses = [self.fitness(chromosome) for chromosome in self.classes]
        total_fitness = sum(fitnesses)
        probabilities = [fitness/total_fitness for fitness in fitnesses]
        parent1 = random.choices(self.classes, weights=probabilities)[0]
        parent2 = random.choices(self.classes, weights=probabilities)[0]
        return parent1, parent2

    def evolve(self):
        # Generate new generation using elitism, selection, crossover, and mutation
        elites = int(self.elitism * self.population_size)
        new_population = []
        # Elitism
        ranked_classes = [(chromosome, self.fitness(chromosome)) for chromosome in self.classes]
        ranked_classes.sort(key=lambda x: x[1], reverse=True)
        for i in range(elites):
            new_population.append(ranked_classes[i][0])
        # Selection, crossover, and mutation
        for i in range(self.population_size - elites):
            parent1, parent2 = self.select_parents()
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            new_population.append(child1)
            new_population.append(child2)
        self.classes = new_population

    def get_best_schedule(self):
        # Return the best schedule in the current generation
        best_chromosome = max(self.classes, key=lambda x: self.fitness(x))
        return best_chromosome

    def save_schedule(self, chromosome):
        # Save the given schedule to the database
        Classes.objects.all().delete()
        for i in range(len(chromosome)):
            room, instructor, course, section,semester, meeting_time = chromosome[i]
            class_data = Classes(room=room, instructor=instructor, course=course, section=section,class_semester=semester, meeting_time=meeting_time)
            class_data.save() 

def Timetable(request):
    # Initialize genetic algorithm with desired parameters
    population_size = 50
    mutation_rate = 0.1
    crossover_rate = 0.8
    elitism = 0.1
    ga = GeneticAlgorithm(population_size, mutation_rate, crossover_rate, elitism)

    # Evolve the population for a certain number of generations
    num_generations = 100
    for i in range(num_generations):
        print("\nGeneration:"+str(i))
        ga.evolve()

    # Get the best schedule from the current population
    best_schedule = ga.get_best_schedule()

    # Save the schedule to the database
    ga.save_schedule(best_schedule)

    # Retrieve the schedule data from the database and pass it to the template
    schedule_data = Classes.objects.all()
    context = {'schedule_data': schedule_data}

    # Render the template with the schedule data
    messages.success(request, 'New Timetable has been successfully generated.')
    return JsonResponse({'status': 'success'})

