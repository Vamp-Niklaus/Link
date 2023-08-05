from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthday = models.DateField()
    gender = models.CharField(
        max_length=11,
        choices=[('Male','Male'),('Female','Female'),('Other','Other')]
    )
    def __str__(self):
        return self.user.username
class link_list(models.Model):
    l_id=models.AutoField(primary_key = True)
    u_id=models.ForeignKey(Users,db_column='u_id', on_delete=models.CASCADE)
    category=models.CharField(max_length=50)
    link=models.CharField(max_length=500)
    name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100,default='none')
    # def __str__(self):
    #     return  self.rby.user.username +", "+self.category