from django.db import models
import re
import datetime, re
import bcrypt


class UserManager(models.Manager):
    def reg_validator(self, form):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        name = form['name']
        email = form['email']
        alias = form['alias']
        birthday = form['birthday']
        password = form['password']
        confirm_pw = form['confirm_password']
        print(birthday)

        
        if len(name) < 2:
            errors['name'] = "Name cannot be blank"
        elif not name.isalpha():
            errors['name'] = "Name cannot contain numbers or special characters!"

        else:
            users = User.objects.filter(alias=alias)
            if len(users) > 0:
                errors['alias'] = "alias already exists. Please login."
      
        if len(alias) < 2:
            errors['alias'] = "Alias cannot be blank"
        elif not alias.isalpha():
            errors['alias'] = "Alias cannot contain number or special characters!"
             
        if len(email) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid email format"
        else:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                errors['email'] = "Email already exists. Please login."
        if not birthday:
            errors['birthday'] = "Please enter a birth date"
        elif birthday > str(datetime.datetime.now()):
            errors['birthday'] = "date is invalid"
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif password != confirm_pw:
            errors['confirm_pw'] = "Passwords do not match"

        return errors

    def loginvalidator(self, form):
        errors = {}
        email = form['email']
        
        password = form['password']
        if len(email) < 0:
            errors["email"] = "Please enter email"
        elif len(User.objects.filter(email=email)) < 1:
            errors['email'] = "Email not in database please register!"
        else:
            if not bcrypt.checkpw(password.encode(), User.objects.get(email=email).password.encode()):
                errors['email'] = "invald email!"

        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, form):

        errors = {}
        title = form['title']
        if len(title) < 1:
            errors["title"] = "Description can't be blank"
        if len(title) < 2:
            errors["title"] = "Description is too short"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    alias = models.EmailField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Quote(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    addedby = models.ForeignKey(
        User, related_name="uploaded_quotes", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = QuoteManager()




