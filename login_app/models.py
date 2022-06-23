from django.db import models
import bcrypt
import re
from datetime import datetime

# Create your models here.
class userManager(models.Manager):
    def basic_validation(self,request_post,user=None):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        page=request_post['btn']
        
        #if email is empty 
        if not request_post['email']:
            errors['email']='Plaese enter email'
        #else if in login form email is wrong (not in db)- 
        #we use (not user) becase if the email exists in db, user will not be empty
        elif not user and page=='Log in': 
            errors['email3']='Email not registerd'
        #else if email format is wrong
        elif not EMAIL_REGEX.match(request_post['email']):
            errors['email2'] = "Invalid email address!"
        #else if user not empty => email exist (login form) 
        elif user:
            #compare the entered pw with pw in the db
            if not bcrypt.checkpw(request_post['pw'].encode(),user[0].pw.encode()):
                errors['wrong_pw']="Password and email does not match"
        
        #if we are at register form
        if page=='Register': 
            
            #if email exist in db
            if User.objects.filter(email=request_post['email']).exists():
                errors['email4']='Email is already registered'
            
            if len(request_post['pw'])<8:
                errors['pw']='Passowrd should be at least 8 characters'
            
            #if it has less than 2 char, or if contains things other than letters    
            if len(request_post['fname'])<2 or not request_post['fname'].isalpha():
                errors['fname']='First name should be at least 2 characters and contains letters only'    
            if len(request_post['lname'])<2 or not request_post['lname'].isalpha():
                errors['lname']='Last name should be at least 2 characters and contains letters only'
            
            #if confirm pw doesnt equal pw
            if request_post['Cpw'] != request_post['pw']:
                errors['C+pw']='Password did not match'    
                
            # if date is empty 
            if not request_post['date']:
                errors['date2']='Please enter Birthdate'
                
            # if the entered date is in the future 
            elif request_post['date']>str(datetime.today()):
                errors['date']='Birthdate should be in the past'
            else:
                datenow = datetime.today()
                birthdate=datetime.strptime(request_post['date'], "%Y-%m-%d").date()
                date = datenow.year - birthdate.year - ((datenow.month, datenow.day) < (birthdate.month, birthdate.day))
                #if age less than 13
                if int(date)<13:
                    errors['date3']='User should be 13 yesrs old at least'
        return errors
    
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    pw=models.CharField(max_length=45)
    date=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects=userManager()
    
class Message(models.Model):
    message=models.TextField()
    user_id=models.ForeignKey(User, related_name='massages' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    comment=models.TextField()
    user_id=models.ForeignKey(User, related_name='comments' ,on_delete=models.CASCADE)
    massage_id=models.ForeignKey(Message, related_name='comments' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)