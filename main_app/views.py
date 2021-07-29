from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Login/Registration
def index(request):
  if "user_id" in request.session:
    return redirect("/dashboard")
  return render(request, "index.html")


# Registration
def register(request):
  errors = User.objects.registration_validator(request.POST)

  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/")
  else:
    hash_slinging_slasher = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
      first_name = request.POST['first_name'], 
      last_name = request.POST['last_name'], 
      email = request.POST['email'], 
      password = hash_slinging_slasher
    )

    request.session['user_id'] = new_user.id
    return redirect("/dashboard")


# Login
def login(request):
  errors = User.objects.login_validator(request.POST)

  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/")
  else:
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    return redirect("/dashboard")


# Logout
def logout(request):
  del request.session['user_id']

  return redirect("/")


# Create Job
def add_job(request):
  if 'user_id' not in request.session:
    return redirect('/')
  context = {
    'user': User.objects.get(id = request.session['user_id']),
    'categories': Category.objects.all()
  }
  return render(request, "new_job.html", context)


def create_job(request):
  if 'user_id' not in request.session:
    return redirect('/')
  errors = Job.objects.job_validator(request.POST)
  user = User.objects.get(id=request.session['user_id'])
  if len(Category.objects.filter(category = request.POST['category_input'])) != 0:
    messages.error(request, "Category already exists.")
    return redirect("/jobs/new")

  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/jobs/new")
  else:
    job = Job.objects.create(
      title = request.POST['title'], 
      description = request.POST['description'], 
      location = request.POST['location'], 
      user = user
    )
    user.jobs_created.add(job)

    if request.POST['category_input'] != "":
      category = Category.objects.create(category = request.POST['category_input'])
      job.categories.add(category)

    if request.POST.getlist('category') != []:
      for cat_id in request.POST.getlist('category'):
        category = Category.objects.get(id = cat_id)
        category.jobs.add(job)
    
  return redirect("/dashboard")


def dashboard(request):
  if 'user_id' not in request.session:
    return redirect('/')
  this_user = User.objects.get(id=request.session['user_id'])
  jobs_added = this_user.jobs_added.all()
  context = {
      'user': this_user,
      'jobs_added': jobs_added,
      'all_jobs': Job.objects.exclude(id__in=jobs_added),
  }
  
  return render(request, 'dashboard.html', context)


def show_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  user = User.objects.get(id=request.session['user_id'])
  job = Job.objects.get(id = job_id)
  categories = Category.objects.all()

  context = {
    'user': user,
    'job': job,
    "categories": categories,
  }
  return render(request, 'view_job.html', context)


def edit_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  job = Job.objects.get(id = job_id)
  user = User.objects.get(id=request.session['user_id'])
  if job.user != user:
    return redirect("/dashboard")
  context = {
    'job': job,
    'user': user,
  }
  return render(request, 'edit_job.html', context)


def update_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  errors = Job.objects.job_validator(request.POST)

  if len(errors) > 0:
    for key, value in errors.items():
        messages.error(request, value)
    return redirect(f"/jobs/edit_job/{job_id}")
  else:
    job_to_edit = Job.objects.get(id = job_id)
    job_to_edit.title = request.POST['title']
    job_to_edit.description = request.POST['description']
    job_to_edit.location = request.POST['location']
    job_to_edit.save()
  return redirect("/dashboard")


def delete_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  user = User.objects.get(id=request.session['user_id'])
  job = Job.objects.get(id = job_id)
  if job.user != user:
    return redirect("/dashboard")
  job.delete()
  return redirect("/dashboard")


def add_job_to_user(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  user = User.objects.get(id = request.session['user_id'])
  job = Job.objects.get(id = job_id)
  user.jobs_added.add(job)
  return redirect("/dashboard")


def give_up_on_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  user = User.objects.get(id = request.session['user_id'])
  job = Job.objects.get(id = job_id)
  user.jobs_added.remove(job)
  return redirect("/dashboard")


def completed_job(request, job_id):
  if 'user_id' not in request.session:
    return redirect('/')
  user = User.objects.get(id = request.session['user_id'])
  job = Job.objects.get(id = job_id)
  if user not in job.other_jobs.all():
    messages.error(request, "You must first add the job to your list before you can complete it.")
    return redirect("/dashboard")
  job.delete()
  return redirect("/dashboard")