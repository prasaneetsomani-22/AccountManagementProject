from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('',views.Login,name = 'Login'),
	path('logout/',views.Logout,name = 'Logout'),
	path('register/',views.Registeration,name = 'Registeration'),
	path('otp_verify/',views.otp_verify,name = 'otp_verify'),
	path('add_account/',views.Add_account,name = 'Add_account'),
	path('admin_role/',views.admin,name='Admin'),
	path('Accounts/',views.Account_list,name = 'Account_list'),
	path('User/<int:pk>/',views.AccountDetails,name = 'AccountDetails'),
	path('Transaction/Edit/<int:param1>/<int:param2>/',views.Edit_details,name = 'Edit_details'),
	path('Transaction/Delete/<int:param1>/<int:param2>/',views.Delete_details,name = 'Delete_details'),
	path('ADD/<int:id1>/',views.Add_transaction,name='Add_transaction'),

	path('reset_password/',auth_views.PasswordResetView.as_view(template_name='Accounts/reset_password.html'),name='reset_password'),
	path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='Accounts/reset_password_sent.html'),name='password_reset_done'),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Accounts/reset.html'),name='password_reset_confirm'),
	path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'),name='password_reset_complete'),

	path('api/',views.apiview,name='api'),
	path('api_update/<int:pk>',views.api_update_view,name='update'),
	path('api/create',views.api_create_view,name='create'),
	path('api_delete/<int:pk>',views.api_delete_view,name='delete'),
]