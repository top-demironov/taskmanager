from django.urls import path

from tasks import views
from tasks.forms import SignupForm

urlpatterns = [
	path('', views.index, name='index'),
	path('projects/', views.projects, name='projects'),
	path('projects/create/', views.create_project, name='projects_create'),
	path('project/<int:project_id>/', views.project, name='project'),
	path('performers/', views.performers, name='performers'),
	path('tasks/', views.tasks, name='tasks'),
	path('tasks/create/', views.create_task, name='tasks_create'),
	path('tasks/<int:task_id>/', views.task, name='task'),

	path('signup/', views.signup, name='signup'),
	path('signin/', views.signin, name='signin'),
	path('signout/', views.signout, name='signout'),
]