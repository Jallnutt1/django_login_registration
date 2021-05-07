from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # EMAIL_REGEX = re.compile(r'^[\S]+@[\S]+\.[a-zA-Z]+$')
        
        if len(postData['fname']) < 2:
            errors['fname'] = "First name must be at least 5 characters"

        if len(postData['lname']) < 2:
            errors['lname'] = "Last name must be at least 5 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = 'Email already exists'

        if len(postData['pwd']) < 8:
            errors['pwd'] = "Your password must be at least 8 characters"
        elif postData['pwd'] != postData['confirm']:
            errors['pwd'] = "Your password did not match the confirm field"
            
        return errors

class User(models.Model):
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

