from django.core.mail import send_mail
import uuid
from django.conf import settings

def send_forget_password_mail(email, token):
   
    subject ='forget password link'
    message =f'Hi, Click on the link to reset your password http://127.0.0.1:8000/ChangePassword.html//{token}'
    email_from=settings.EMAIL_HOST_USER
    recepient_list=[email]
    send_mail(subject, message, email_from, recepient_list)
    return True
