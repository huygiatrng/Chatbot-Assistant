from django.db import models

# Create your models here.
class UserDetails(models.Model):
	Firstname = models.CharField(max_length=100 ,default = None)
	Lastname = models.CharField(max_length=100 ,default = None)
	Number =  models.CharField(max_length=100 ,default = None)
	Email = models.CharField(max_length=100 ,default = None)
	Username = models.CharField(max_length=100 ,default = None)
	Password = models.CharField(max_length=100 ,default = None)

	class Meta:
		db_table = 'UserDetails'