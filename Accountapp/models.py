from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	Account_number = models.CharField(max_length = 20)
	Account_holder_name = models.CharField(max_length = 20)
	Account_balance = models.IntegerField(default = 0,null=True)
	
	def __str__(self):
		return self.Account_number


class Transactions(models.Model):
	T_choices = (
		("CHOOSE","choose"),
		("CREDITED","credited"),
		("DEBITED","debited")
	)
	from_account = models.ForeignKey(Account,on_delete=models.CASCADE)
	amount = models.IntegerField()
	description = models.CharField(max_length=50)
	transaction_type = models.CharField(max_length= 10,choices=T_choices,default="CHOOSE")
	#transaction_date = models.DateField()

	def __str__(self):
		return str(self.from_account)
# Create your models here.
