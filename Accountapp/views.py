from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import Account,Transactions
from .forms import EditForm,AddForm,RegisterForm,AccountForm,OTPform
from django.contrib.auth.models import User,Group
from .filter import TransFilter
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .decorators import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sms_auth import verifications,verification_checks
from .serializers import AccountSerializer

@unauthorized_user
def Registeration(request):
	form = RegisterForm()

	if request.method == "POST":
		form  = RegisterForm(request.POST)
		if form.is_valid():
			# user = form.save()
			# group = Group.objects.get(name="customer")
			# user.groups.add(group)
			# return redirect('Login')
			request.session['user'] = form.cleaned_data
			request.session['number'] = form.cleaned_data['Phone_number']
			verifications(request.session['number'])
			return redirect('otp_verify')
	return render(request,'Accounts/Register.html',{'form':form})


def otp_verify(request):
	form = OTPform()
	if request.method == "POST":
		form = OTPform(request.POST)
		if form.is_valid():
			otp = form.cleaned_data['otp']
			status = verification_checks(request.session['number'],otp).status
			if status == 'approved':
				user = User.objects.create_user(request.session['user']['username'],
				request.session['user']['email'],request.session['user']['password1'])
				group = Group.objects.get(name="customer")
				user.groups.add(group)
				return redirect('Login')
			else:
				return HttpResponse('otp not matched')
		
		

	return render(request,'Accounts/otp_verify.html',{'form':form})

@login_required(login_url='Login')
@user_role(allowed_user=['customer'])
def Add_account(request):
	form = AccountForm()
	if request.method == 'POST':
		form = AccountForm(request.POST)
		if form.is_valid():
			account = form.save(commit=False)
			account.user = request.user
			account.save()
			return redirect('Account_list')
	else:
		form = AccountForm()
	return render(request,'Accounts/AddAccount.html',{'form':form})

@login_required(login_url='Login')
# @user_role(allowed_user=['admin'])
def admin(request):
	account = Account.objects.all()
	users = User.objects.all()
	transaction = Transactions.objects.all()
	context = {
		'account':account,
		'users':users,
		'transaction':transaction,
	}
	return render(request,'Accounts/admin.html',context)

@login_required(login_url='Login')
@admin_only
def Account_list(request):
	account = Account.objects.filter(user=request.user)

	return render(request, 'Accounts/Account_list.html',{'account':account,})

@unauthorized_user
def Login(request):
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('Account_list')
	context = {}
	return render(request,'Accounts/login.html',context)

def Logout(request):
	logout(request)
	return redirect('Login')

@login_required(login_url='Login')
@user_role(allowed_user=['customer'])
def AccountDetails(request,pk):
	details = Account.objects.get(pk=pk)
	# acc = details.Account_number
	transactions = Transactions.objects.filter(from_account=details)
	myFilter = TransFilter(request.GET, queryset = transactions)
	transactions = myFilter.qs
	return render(request, 'Accounts/details.html',{'details':details,'transactions':transactions,'filter':myFilter})

@login_required(login_url='Login')
@user_role(allowed_user=['customer'])
def Edit_details(request, param1, param2):
	get = Transactions.objects.get(pk=param2)
	if request.method == 'POST':
		form = EditForm(request.POST,instance=get)
		if form.is_valid():
			form.save()
			return redirect('AccountDetails',param1)
			
	else:
		form = EditForm(instance=get)
	return render(request,'Accounts/edit_details.html',{'form': form})



@login_required(login_url='Login')
@user_role(allowed_user=['customer'])
def Delete_details(request, param1, param2):
	
	if request.method == 'POST':
		get = Transactions.objects.get(pk=param2)
		get.delete()
		return redirect('AccountDetails',param1)

	return render(request,'Accounts/delete_details.html')


@login_required(login_url='Login')
@user_role(allowed_user=['customer'])
def Add_transaction(request,id1):
	get = Account.objects.get(pk=id1)
	if request.method == 'POST':
		form = AddForm(request.POST)
		if form.is_valid():
			transaction = form.save(commit=False)
			transaction.from_account = get
			transaction.save()
			if transaction.transaction_type == "CREDITED":
				 get.Account_balance += transaction.amount
				 get.save()
			else:
				get.Account_balance -= transaction.amount
				get.save()
			return redirect('AccountDetails',id1)
	else:
		form = AddForm()
	return render(request,'Accounts/add.html',{'form': form})

@api_view(['GET',])
def apiview(request):
	accounts = Account.objects.all()
	serializer = AccountSerializer(accounts, many=True)
	return Response(serializer.data)


@api_view(['PUT',])
def api_update_view(request, pk):
	try:
		account = Account.objects.get(pk=pk)
	except Account.DoesNotExists:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	data = {}
	if request.method == 'PUT':
		serializer = AccountSerializer(account, data=request.data)
		if serializer.is_valid():
			serializer.save()
			data['success'] = 'Successful'
		else:
			data['failure'] = 'Failed'
	return Response(data=data)

@api_view(['POST',])
def api_create_view(request):
	
	data = {}
	if request.method == 'POST':
		
		serializer = AccountSerializer(data=request.data)

		if serializer.is_valid():
			serializer.user = request.user
			serializer.save()
			data['success'] = 'Successful Added'
		else:
			data['failure'] = 'Failed to Add'
	return Response(data=data)


@api_view(['DELETE',])
def api_delete_view(request, pk):
	
	data = {}
	if request.method == 'DELETE':
		account = Account.objects.get(pk=pk)
		account.delete()
		return Response('Successfuly deleted')

		
	