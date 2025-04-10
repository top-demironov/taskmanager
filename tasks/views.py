from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from tasks.forms import TaskCreateForm, TaskForm, SignupForm
from tasks.models import Project, User, Task, TaskStatus


def index(request):
	return render(request, 'tasks/index.html')


@login_required
def projects(request):
	projects_list = Project.objects.all()
	return render(request, 'tasks/project/list.html', context={'projects': projects_list})


@login_required
def project(request, project_id):
	project_view = Project.objects.get(pk=project_id)
	tasks_list = Task.objects.filter(project_id=project_id)
	return render(request, 'tasks/project/details.html', context={'project': project_view, 'tasks': tasks_list})


@login_required
def create_project(request):
	if request.method == 'POST':
		name = request.POST['name']
		description = request.POST['description']
		project_view = Project.objects.create(name=name, description=description)
		return redirect('project', project_view.id)
	return render(request, 'tasks/project/create.html')


@login_required
def performers(request):
	performers_list = User.objects.all()
	return render(request, 'tasks/performers.html', context={'performers': performers_list})


@login_required
def tasks(request):
	tasks_list = Task.objects.all()
	return render(request, 'tasks/task/list.html', context={'tasks': tasks_list})


@login_required
def task(request, task_id):
	task_view = Task.objects.get(pk=task_id)  # Получаем объект Task по первичному ключу
	if request.method == "POST":
		form = TaskForm(request.POST, instance=task_view)  # Передаём существующий объект в форму
		if form.is_valid():
			form.save()
			return redirect('tasks')
	else:
		form = TaskForm(instance=task_view)  # Предзаполняем форму текущими данными
	return render(request, 'tasks/task/details.html', {'form': form, 'task': task})


@login_required
def create_task(request):
	if request.method == "POST":
		form = TaskCreateForm(request.POST)
		if form.is_valid():
			# form.save()  # В случае если не нужно изменять сущность задачи
			task_view = form.save(commit=False)
			task_view.status = TaskStatus.objects.get(name="Новая")
			task_view.save()
			return redirect('tasks')
	else:
		form = TaskCreateForm()

	projects_list = Project.objects.all()
	return render(request, 'tasks/task/create.html', context={'form': form, 'projects': projects_list})


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])  # Хэшируем пароль
			user.save()
			return redirect('signin')
	else:
		form = SignupForm()
	return render(request, 'auth/signup.html', {'form': form})


def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		# Аутентификация пользователя
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)  # Вход пользователя
			return redirect('index')  # Перенаправление после успешного входа
		else:
			# Ошибка входа
			return render(request, 'auth/signin.html', {'error': 'Неверный логин или пароль'})
	return render(request, 'auth/signin.html')


@login_required
def signout(request):
	# Выходим из системы
	logout(request)
	# Перенаправляем пользователя на страницу входа
	return redirect('signin')

