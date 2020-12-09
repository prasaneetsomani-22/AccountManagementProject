import django_filters
from .models import Transactions
from django_filters import CharFilter

class TransFilter(django_filters.FilterSet):
	description = CharFilter(field_name="description",lookup_expr='icontains')
	class Meta:
		model = Transactions
		fields = ['transaction_type']