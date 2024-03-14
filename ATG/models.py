import datetime
import json
from django.db import models
# Abstract User Model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractBaseUser):
    
    u_name = models.CharField(max_length=100)
    u_email = models.EmailField(max_length=100, primary_key=True)
    u_gender=models.CharField(max_length=40,null=True,blank=True)
    u_department=models.CharField(max_length=50,null=True,blank=True)
    u_password = models.CharField(max_length=100)
    u_contactNo=models.CharField(max_length=15, null=True, validators=[RegexValidator(
    regex=r'^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$',
    message='Phone number must be in the format 00923XX-XXX-XXXX',
)])
    u_profile_pic=models.FileField(upload_to='StoreProfilePic/', null=True, default=None)
    u_city=models.CharField(max_length=30, null=True)
    id = models.IntegerField(primary_key=False)
   
   
    def save(self, *args, **kwargs):
        if not self.id:
            last_obj = self.__class__.objects.order_by('id').last()
            self.id = last_obj.id + 1 if last_obj else 1
        super(User, self).save(*args, **kwargs)

    # create a custom user manager
    objects = BaseUserManager()

    class Meta:
        abstract = True
    def __str__(self):
        return self.name

class Admin(User):
    class Meta:
        db_table="Admin"
    def __str__(self):
        return self.name
class Courses(models.Model):
    c_name = models.CharField(max_length=100)
    c_code = models.CharField(max_length=100, primary_key=True)
    max_numb_students = models.CharField(max_length=65)
    c_semester = models.CharField(max_length=100)
    c_section=models.CharField(max_length=100)
    c_type = models.CharField(max_length=40)
    instructors = models.ManyToManyField('Faculty', blank=True)
    id = models.IntegerField(primary_key=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_obj = self.__class__.objects.order_by('id').last()
            self.id = last_obj.id + 1 if last_obj else 1
        super(Courses, self).save(*args, **kwargs)

    class Meta:
        db_table = "Courses"
        unique_together = (('c_name', 'c_code'),)

    def __str__(self):
        return self.c_name

class Certificate(models.Model):
    file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return self.file.name
class UploadedFile(models.Model):
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.file_path

class Faculty(User):
    f_startTimePref = models.TimeField(null=True, blank=True)
    f_endTimePref = models.TimeField(null=True, blank=True)
    f_RoomPref = models.CharField(max_length=100, null=True, blank=True)
    f_CoursePref = models.CharField(max_length=40, null=True)
    f_ApprovalStatus = models.CharField(max_length=100, null=True, blank=True)
    f_Comment = models.CharField(max_length=100, null=True, blank=True)
    f_courses = models.ManyToManyField(Courses, blank=True, related_name='course_instructors')
    f_certificates = models.ManyToManyField(Certificate)
    
    class Meta:
        db_table = "Faculty"

    def __str__(self):
        return self.u_email

class FreferenceEnable(models.Model):
    startDatetime=models.DateTimeField(null=True)
    endDatetime=models.DateTimeField(null=True)
    class Meta:
        db_table='freferenceenable'

class Students(User):
    s_session=models.CharField(max_length=20)
    s_section=models.CharField(max_length=50)
    s_semester=models.CharField(max_length=10)

    class Meta:
     db_table="Students"
    def __str__(self):
        return self.name


class Meetings(models.Model):
    time = models.CharField(max_length=50)
    day = models.CharField(max_length=15)
    
    class Meta:
        db_table="Meetings"

    def __str__(self):
        return self.name

    @staticmethod
    def generate_meetings(table_instance):
    # Set the start time, off time, and slot time
        start_time = datetime.datetime.strptime(table_instance.StartTime, '%H:%M').time()
        off_time = datetime.datetime.strptime(table_instance.OffTime, '%H:%M').time()
        slot_time = datetime.datetime.strptime(table_instance.SlotTime, '%H:%M').time()

        # Calculate the number of slots per day
        num_slots = int((datetime.datetime.combine(datetime.date.today(), off_time) - datetime.datetime.combine(datetime.date.today(), start_time)).seconds / (slot_time.hour * 60 * 60 + slot_time.minute * 60))

        # Generate meetings for each day
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        start_day = days.index(days[0])
        end_day = days.index(days[4])
        Meetings.objects.all().delete()
        for i in range(start_day, end_day+1):
            day_name = days[i]
            for j in range(num_slots):
                slot_start = datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=j * (slot_time.hour * 60 + slot_time.minute))
                slot_end = slot_start + datetime.timedelta(minutes=slot_time.hour * 60 + slot_time.minute)
                meeting_time = f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                meeting = Meetings.objects.create(time=meeting_time, day=day_name)
                meeting.save()



class Rooms(models.Model):
    r_name=models.CharField(max_length=100, primary_key=True)
    r_type=models.EmailField(max_length=100)
    r_department=models.CharField(max_length=20)
    r_capacity=models.CharField(max_length=100)
    id = models.IntegerField(primary_key=False)
    def save(self, *args, **kwargs):
        if not self.id:
            last_obj = self.__class__.objects.order_by('id').last()
            self.id = last_obj.id + 1 if last_obj else 1
        super(Rooms, self).save(*args, **kwargs)
    class Meta:
        db_table="Rooms"
    def __str__(self):
        return self.name



class Sections(models.Model):
    section_name = models.CharField(max_length=50, primary_key=True)
    courses = models.ManyToManyField(Courses)
    id = models.IntegerField(primary_key=False)
    def save(self, *args, **kwargs):
        if not self.id:
            last_obj = self.__class__.objects.order_by('id').last()
            self.id = last_obj.id + 1 if last_obj else 1
        super(Sections, self).save(*args, **kwargs)
    
    @property
    def get_courses(self):
        return self.courses
    
    class Meta:
        db_table="Sections"

    def __str__(self):
        return self.section_name


class Semesters(models.Model):
    semester_no = models.CharField(max_length=25)
    sem_section = models.ForeignKey(Sections, on_delete=models.CASCADE, db_column='section_name', default=None, related_name='sem_section')
    num_class_in_week = models.IntegerField(default=0)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    meeting_time = models.ForeignKey(Meetings, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE, blank=True, null=True)
    instructor = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True, null=True)
    def set_room(self, room):
        semester = Semesters.objects.get(pk = self.semester_no)
        semester.room = room
        semester.save()

    def set_meetingTime(self, meetingTime):
        semester = Semesters.objects.get(pk = self.semester_no)
        semester.meeting_time = meetingTime
        semester.save()

    def set_instructor(self, instructor):
        semester = Semesters.objects.get(pk=self.section_id)
        semester.instructor = instructor
        semester.save()
    class Meta:
     db_table="Semesters"
    unique_together = (('semester_no', 'section'),)
    def __str__(self):
        return self.semester_no

        
class Table(models.Model):
    Department=models.CharField(max_length=30)
    Section=models.CharField(max_length=30)
    Shift=models.CharField(max_length=30)
    StartTime=models.CharField(max_length=30)
    OffTime=models.CharField(max_length=30)
    SlotTime=models.CharField(max_length=30)
    class Meta:
     db_table="Table"
    def __str__(self):
        return self.name

class Classes(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE,related_name='room')
    instructor = models.ForeignKey(Faculty, on_delete=models.CASCADE,related_name='instructor')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,related_name='course')
    section = models.ForeignKey(Sections, on_delete=models.CASCADE,related_name='section')
    class_semester = models.ForeignKey(Semesters, on_delete=models.CASCADE,related_name='class_semester', default=None)
    meeting_time = models.ForeignKey(Meetings, on_delete=models.CASCADE, related_name='meeting_time')
    class Meta:
     db_table="Classes"

class users(models.Model):
    v_email=models.EmailField(max_length=100, primary_key=True)
    v_password = models.CharField(max_length=100, null=True)
    
    
    class Meta:
        db_table="users"
    def __str__(self):
        return self.name
    
class CourseFaculty(models.Model):
    Subject=models.ForeignKey(Courses, on_delete=models.CASCADE,related_name='subject')
    Teacher = models.ForeignKey(Faculty, on_delete=models.CASCADE,related_name='Teacher')
    # Section = models.ForeignKey(Sections, on_delete=models.CASCADE,related_name='Section')
    class Meta:
        db_table="CourseFaculty"
    def __str__(self):
        return self.Subject

class Help(models.Model):
    time = models.CharField(max_length=20, default=None)
    class Meta:
        db_table='help'
    def __str__(self):
        return self.name

    @staticmethod
    def generate_slottime(table_instance):
    # Set the start time, off time, and slot time
        start_time = datetime.datetime.strptime(table_instance.StartTime, '%H:%M').time()
        off_time = datetime.datetime.strptime(table_instance.OffTime, '%H:%M').time()
        slot_time = datetime.datetime.strptime(table_instance.SlotTime, '%H:%M').time()

        # Calculate the number of slots per day
        num_slots = int((datetime.datetime.combine(datetime.date.today(), off_time) - datetime.datetime.combine(datetime.date.today(), start_time)).seconds / (slot_time.hour * 60 * 60 + slot_time.minute * 60))

        # Generate meetings for each day
        # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        # start_day = days.index(days[0])
        # end_day = days.index(days[4])
        Help.objects.all().delete()
        for i in range(num_slots):
            slot_start = datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=i * (slot_time.hour * 60 + slot_time.minute))
            slot_end = slot_start + datetime.timedelta(minutes=slot_time.hour * 60 + slot_time.minute)
            meeting_time = f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
            help = Help.objects.create(time=meeting_time)
            help.save()