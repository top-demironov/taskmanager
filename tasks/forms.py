from django import forms
from .models import Task, User


class TaskCreateForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['project', 'title', 'description', 'due_date']

		widgets = {
			'project': forms.Select(attrs={
				'class': 'form-select',
				'id': 'floatingProjectSelect',
				'aria-label': 'Выбор проекта для привязки задачи',
				'required': True
			}),
			'title': forms.TextInput(attrs={
				'class': 'form-control',
				'id': 'floatingTitle',
				'placeholder': 'Очень простая задача',
				'required': True
			}),
			'description': forms.TextInput(attrs={
				'class': 'form-control',
				'id': 'floatingDescription',
				'placeholder': 'Нужно сделать несколько пунктов...',
				'required': True
			}),
			'due_date': forms.DateInput(attrs={
				'class': 'form-control',
				'id': 'floatingDueDate',
				'type': 'date',
				'required': True
			}),
		}


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['project', 'title', 'description', 'due_date', 'status']  # Все поля, которые можно редактировать
		widgets = {
			'project': forms.Select(attrs={'class': 'form-select'}),
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'status': forms.Select(attrs={'class': 'form-select'}),
		}


class SignupForm(forms.ModelForm):
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
				'class': 'form-control',
				'id': 'floatingPasswordConfirm',
				'placeholder': 'Подтверждение пароля',
				'required': True
			}))

	class Meta:
		model = User
		fields = ['firstname', 'lastname', 'username', 'email', 'password']

		widgets = {
			'firstname': forms.TextInput(attrs={
				'class': 'form-control',
				'id': 'floatingTitle',
				'placeholder': 'Очень простая задача',
				'required': True
			}),
			'lastname': forms.TextInput(attrs={
				'class': 'form-control',
				'id': 'floatingLastname',
				'aria-label': 'Фамилия',
				'placeholder': 'Очень простая задача',
				'required': True
			}),
			'username': forms.TextInput(attrs={
				'class': 'form-control',
				'id': 'floatingUsername',
				'placeholder': 'Логин пользователя',
				'aria-label': 'Логин пользователя',
				'required': True
			}),
			'email': forms.EmailInput(attrs={
				'class': 'form-control',
				'id': 'floatingEmail',
				'placeholder': 'Почта',
				'required': True
			}),
			'password': forms.PasswordInput(attrs={
				'class': 'form-control',
				'id': 'floatingPassword',
				'placeholder': 'Пароль',
				'required': True
			}),
		}

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError('Пароли не совпадают!')
		return cleaned_data

