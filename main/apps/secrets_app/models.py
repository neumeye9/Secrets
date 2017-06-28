from __future__ import unicode_literals

from django.db import models

import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

# Create your models here.

class UsersManager(models.Manager):
    def add(self, first_name, last_name, email, password, confirm):
        
        messages = []

        if len(first_name) < 1:
            messages.append('You must enter a First Name to Register')
        if not first_name.isalpha():
            messages.append('First Name must contain letters only')
        if len(last_name) < 1:
            messages.append('You must enter a Last Name to Register')
        if not last_name.isalpha():
            messages.append('Last Name must contain letters only')
        if len(email) < 1:
            messages.append('You must enter an email to Register')
        if not EMAIL_REGEX.match(email):
            messages.append('Not a valid Email Address') 
        if len(email) > 1:
            check = Users.usersManager.filter(email=email)
            if len(check) > 0:
                messages.append('Email already registered')
        if len(password) < 1:
            messages.append('You must enter a Password to Register')
        if len(password) < 8:
            messages.append('For added security, please select a password that is atleast 8 characters')
        if password != confirm:
            messages.append('Password and Password Confirmation do not match')
        
        if len(messages) > 0:
            return False, messages
        
        else:
            pw_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            user = Users.usersManager.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            return True, user
    
    def log(self, email, password):

        messages = []

        user = Users.usersManager.filter(email=email)

        if len(email) == 0:
            messages.append('You must enter an email to login')
        if not EMAIL_REGEX.match(email):
            messages.append('Email enteres is not a valid email format')
        if len(user) < 1:
            messages.append('User does not exist, please register')
        
        realpassword = user[0].password
        print realpassword
        hash_check = bcrypt.hashpw(password.encode(), realpassword.encode())

        if realpassword != hash_check:
            messages.append('Password entered does not match')
        
        if len(messages) > 0:
            return False, messages
        
        else:
            return True, user[0]
    

class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usersManager = UsersManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Secrets(models.Model):
    content = models.CharField(max_length=150)
    creator = models.ForeignKey(Users, related_name='secrets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    user = models.ForeignKey(Users, related_name='likes')
    secret = models.ForeignKey(Secrets, related_name='likes')

    

