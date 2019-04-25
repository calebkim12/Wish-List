from django.db import models
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, data):
        errors = {}
         
        if len(data['name']) < 3:
            errors['name'] = 'Name must be at least 3 characters'
        
        if len(data['username']) < 3:
            errors['username'] = 'Username must be at least 3 characters'

        else:
            if len(User.objects.filter(username=data['username'])) > 0:
                errors['username'] = 'Username already exists, please log in'

            
        if len(data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        elif data['password'] != data['confirmpw']:
            errors['password'] = 'Passwords must match'
        return errors


    def login_validator(self, data):
        errors = {}

        if len(User.objects.filter(username=data['username'])) > 1:
            errors['username'] = 'Username already exists'

        elif len(User.objects.filter(username=data['username'])) == 0:
            errors['username'] = 'Please register with us before attempting to log in '

        else:
            user = User.objects.get(username=data['username'])
            if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                errors['password'] = 'Your password was incorrect, Please try again'
        return errors


class ItemManager(models.Manager):
    def item_validator(self, data):
        errors = {}

        if len(data['item']) == 0:
            errors['item'] = 'Please pick an item'
        elif len(data['item']) < 3: 
            errors['item'] = 'Item must be at least 3 characters'
        
        return errors 


      

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='item', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemManager()