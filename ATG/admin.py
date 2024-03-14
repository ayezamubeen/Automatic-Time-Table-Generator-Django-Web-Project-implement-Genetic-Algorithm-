from django.contrib import admin
from .models import Admin,Faculty,Students,Rooms,Courses
# Register your models here.
admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(Students)
admin.site.register(Rooms)
admin.site.register(Courses)
