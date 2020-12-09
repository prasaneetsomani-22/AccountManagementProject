from django import forms
from .models import Transactions,Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EditForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ('from_account','amount','description','transaction_type')

class AddForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = ('amount','description','transaction_type')

class RegisterForm(UserCreationForm):

	Phone_number = forms.CharField(max_length = 13)

	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('Account_number','Account_holder_name','Account_balance')

class OTPform(forms.Form):
	otp = forms.CharField(max_length=6)