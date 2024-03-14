from django.contrib import admin
from django.urls import path
from ATG import views
from .views import delete_certificate
urlpatterns = [

# Home URLs

    path("", views.Home, name='Home'),
    path("Home.html", views.Home, name='Home'),
    path("signupOptions.html", views.signupOptions, name='signupOptions'),
    path("Quicktour.html", views.Quicktour, name='Quicktour'),
    path("Aboutus.html", views.Aboutus, name='Aboutus'),
    path("Contactus.html", views.Contactus, name='Contactus'),
    path("help.html", views.help, name='help'),
    path("ForgetPassword.html", views.ForgetPassword, name='ForgetPassword'),
    path("ChangePassword.html", views.ChangePassword, name='ChangePassword'),
    path("FormForgetPassword.html", views.FormForgetPassword, name='FormForgetPassword'),
    path("Contact_email", views.Contact_email, name='Contact_email'),

# Admin URLs

    path("admin_dashboard.html", views.admin_dashboard, name='admin_dashboard'),
    path("rooms.html", views.room, name='room'),
    path("courses.html", views.courses, name='courses'),
    path('sections.html',views.sections, name='section'),
    path('semesters.html', views.semesters, name='semesters'),
    path("faculty.html", views.faculty, name='faculty'),
    path("students.html", views.students, name='students'),
    path("generate_timetable.html", views.generate_timetable, name='generate_timetable'),
    path("viewTimetable.html", views.viewTimetable, name='viewTimetable'),
    path("editProfile.html", views.editProfile, name='editProfile'),
    path("a_saveeditfrofile", views.a_saveeditfrofile, name='a_saveeditfrofile'),
    path("check_approval_status.html",views.check_approval_status, name='check_approval_status'),

    path("add_room", views.add_room, name='add_room'),
    path('del_room/<int:id>/', views.del_room, name='del_room'),
    path("edit_room/<int:id>", views.edit_room, name='edit_room'),

    path("add_course", views.add_course, name='add_course'),
    path('del_course/<int:id>', views.del_course, name='del_course'),
    path("edit_course/<int:id>", views.edit_course, name='edit_course'),

    path('add_section', views.add_section, name='add_section'),
    path('edit_section/<int:id>', views.edit_section, name='edit_section'),
    path('del_section/<int:id>', views.del_section, name='del_section'),

    path('add_semester', views.add_semester, name='add_semester'),
    path('edit_semester/<int:id>', views.edit_semester, name='edit_semester'),
    path('del_semester/<int:id>', views.del_semester, name='del_semester'),


    path("add_faculty", views.add_faculty, name='add_faculty'),
    path('del_faculty/<int:id>', views.del_faculty, name='del_faculty'),
    path("edit_faculty/<int:id>", views.edit_faculty, name='edit_faculty'),
    path("mail_faculty/<int:id>", views.mail_faculty, name='mail_faculty'),
    path("response_mail_faculty/<int:id>", views.response_mail_faculty, name='response_mail_faculty'),

    path('add_student', views.add_student, name='add_student'),
    path('del_student/<int:id>', views.del_student, name='del_student'),
    path("edit_student/<int:id>", views.edit_student, name='edit_student'),
    path("mail_student/<int:id>", views.mail_student, name='mail_student'),

    path('add_details', views.save_details, name='save_details'),
    path('allocation', views.allocation, name='allocation'),
    path('generate', views.generate, name='generate'),

#Timetable Urls
    path('Timetable', views.Timetable, name='Timetable'),

#Faculty URLs
    path('FacultyEditProfile.html', views.FacultyEditProfile, name='FacultyEditProfile'),
    path('FacultyGiveApproval.html', views.FacultyGiveApproval, name='FacultyGiveApproval'),
    path('FacultyGivePrefernces.html', views.FacultyGivePrefernces, name='FacultyGivePrefernces'),
    path('FacultyViewtimetable.html', views.FacultyViewtimetable, name='FacultyViewtimetable'),
    path('f_saveeditfrofile', views.f_saveeditfrofile, name='EditProfile'),
    path('prefrencefunction', views.prefrencefunction, name='prefrencefunction'),
    path('referencefunt', views.referencefunt, name='referencefunt'),
    path('f_giveaproval', views.f_giveaproval, name='f_giveaproval'),
    path('fsavebtn', views.fsavebtn, name='fsavebtn'),
    path('f_g_prefrences', views.f_g_prefrences, name='f_g_prefrences'),
    path('certificates/<int:certificate_id>/delete/', delete_certificate, name='delete_certificate'),
    path('search-timetable', views.search_timetable, name='search_timetable'),
    path('MainFacultyPage.html', views.MainFacultyPage, name='MainFacultyPage'),
    path('Replace_lecture_Slot', views.Replace_lecture_Slot, name='Replace_lecture_Slot'),

# Student URLs
    path("StudentEditProfile.html", views.StudentEditProfile, name='StudentEditProfile'),
    path("sviewtimetable.html", views.sviewtimetable, name='sviewtimetable'),
    path('ssavebtn', views.ssavebtn, name='ssavebtn'),
#signup of admin
   path("signup_admin", views.signup_admin, name='signup_admin'),  
#signup of faculty
   path("signup_faculty", views.signup_faculty, name='signup_faculty'), 
#signup of student
    path("signup_student", views.signup_student, name='signup_student'),
#login
    path("login", views.login, name='login') ,
#logout
  path('logout_view', views.logout_view, name='logout_view'),
    
]