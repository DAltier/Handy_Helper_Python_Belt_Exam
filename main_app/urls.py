from django.urls import path
from . import views

urlpatterns = [
  
  # User paths
  path('', views.index),
  path('register', views.register),
  path('login', views.login),
  path('logout', views.logout),


  # Create new job 
  path('jobs/new', views.add_job),
  path('jobs/create', views.create_job),

  # Read all jobs
  path('dashboard', views.dashboard),
  # Read one job
  path('jobs/<int:job_id>', views.show_job),

  # Update job
  path('jobs/edit_job/<int:job_id>', views.edit_job),
  path('jobs/update_job/<int:job_id>', views.update_job),

  # Destroy job
  path('jobs/delete_job/<int:job_id>', views.delete_job),


  # Add a job to current user
  path('jobs/add_to_user/<int:job_id>', views.add_job_to_user),
  # Give up on a job
  path('jobs/cancel_job/<int:job_id>', views.give_up_on_job),
  # Job completed
  path('jobs/done_job/<int:job_id>', views.completed_job)
]