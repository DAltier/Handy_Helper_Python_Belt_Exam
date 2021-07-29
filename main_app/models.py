from django.db import models
from datetime import date, datetime
import re
import bcrypt


# User Manager
class UserManager(models.Manager):


  # Registration Validation
  def registration_validator(self, post_data):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    LETTER_REGEX = re.compile(r'^[a-zA-Z]*$')


    # Validate Name Data
    if not LETTER_REGEX.match(post_data['first_name']) or len(post_data['first_name']) < 2 :
      errors['first_name'] = "The first name field is required and should be at least 2 letters long."
    if not LETTER_REGEX.match(post_data['last_name']) or len(post_data['last_name']) < 2:
      errors['last_name'] = "The last name field is required and should be at least 2 letters long."


    # Validate Email Data
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = "Invalid or missing email address!"
    else:
      user_list = User.objects.filter(email = post_data['email'])
      if len(user_list) > 0:
        errors['email'] = "Email is already in use."


    # Validate Password Data
    if len(post_data['password']) < 8:
      errors['password'] = "The password field is required and should be at least 8 characters long."
    if post_data['password'] != post_data['confirm_password']:
      errors['confirm_password'] = "The passwords do not match, try again!"


    return errors


  # Login Validation
  def login_validator(self, post_data):
    errors = {}

    user_list = User.objects.filter(email = post_data['email'])
    if len(user_list) > 0:
      user = user_list[0]
      if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
        errors['password'] = "Invalid Credentials"
    else:
      errors['email'] = "Invalid Credentials"
      
    return errors


# User Model
class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()


# Category manager
class CategoryManager(models.Manager):
  def category_validator(self, post_data):
    errors = {}

    # Validate Category Data
    if len(post_data['category']) < 3:
      errors['category'] = 'Category is required and should be at least 3 characters long.'

    return errors


# Category Model
class Category(models.Model):
  category = models.CharField(max_length = 255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


# Job Manager
class JobManager(models.Manager):
  def job_validator(self, post_data):
    errors = {}


    # Validate Title Data
    if len(post_data['title']) < 3:
      errors['title'] = "Job title is required and should be at least 3 characters long."


    # Validate Description Data
    if len(post_data['description']) < 3:
      errors['description'] = "Job description is required and should be at least 3 characters long."

    # Validate Location Data
    if len(post_data['location']) < 3:
      errors['location'] = "Job location is required and should be at least 3 characters long."

    return errors


# Job Model
class Job(models.Model):
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name="jobs_created", on_delete=models.CASCADE)
  other_jobs = models.ManyToManyField(User, related_name="jobs_added")
  categories = models.ManyToManyField(Category, related_name="jobs")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = JobManager()
