

from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    GENDER_CHOICES = (('m', '男'), ('w', '女'))
    id = models.AutoField(primary_key=True, verbose_name='id')
    user_name = models.CharField(max_length=20, verbose_name='姓名', null=False)
    age = models.IntegerField(verbose_name='年龄')
    # sex = models.CharField(choices=GENDER_CHOICES, max_length=2, verbose_name='性别')
    sex = models.CharField(max_length=2, verbose_name='性别')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    address = models.CharField(max_length=200, verbose_name='地址')

    class Meta:
        db_table = "t_user"
        ordering = ('-update_time',)

    def __str__(self):
        return self.id, self.user_name, self.age, self.sex, self.create_time, self.address