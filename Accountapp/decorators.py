from django.http import HttpResponse
from django.shortcuts import redirect

def unauthorized_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('Account_list')
		else:
			return view_func(request, *args, **kwargs)
		return view_func(request, *args, **kwargs)

	return wrapper_func

def user_role(allowed_user=[]):
	def decorators(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_user:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("You are not Authorized to this Page")
			return view_func(request, *args, **kwargs)
		return wrapper_func
	return decorators

def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'admin':
			return redirect('ProgrammingError at /api/Admin')	

		if group == 'customer':
			return view_func(request, *args, **kwargs)

	return wrapper_func