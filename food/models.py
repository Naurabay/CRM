import jwt
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager



# Create your models here.

class Table(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, *args, **kwargs):
        if login is None:
            raise TypeError('Register your login')


        if not email:
            raise ValueError('Please register your email address')

        user = self.model(
            login=login,
            email=self.normalize_email(email),
            *args,
            **kwargs)


        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, login, email, password=None, *args, **kwargs):

        user = self.model(
            login=login,
            email=self.normalize_email(email),
            *args,
            **kwargs)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    login = models.CharField('Логин', max_length=50, unique=True, db_index=True)
    role= models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Должность', null=True)
    phone = models.CharField('Номер телефона', max_length=100)
    # date_of_add = models.DateTimeField('Дата добавления', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now)
    password = models.CharField(max_length=120, blank=False)

    objects = UserManager()
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email','phone','password' ]

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


    def __str__(self):
        return self.login

    @property
    def token(self):
        return self._generate_jwt_token()


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


class MealCategories(models.Model):
    name = models.CharField(max_length=100, default='еда')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='Department')



class Status(models.Model):
    name = models.CharField(max_length=100, default='Unknown')



class ServicePercentage(models.Model):
    percentage = models.FloatField(default='-')


class Meal(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MealCategories, on_delete=models.CASCADE)
    price = models.FloatField('Price tag')
    description = models.TextField(default='--------------')



class Order(models.Model):
    waiterid = models.IntegerField(default=0)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table', null=True)
    isitopen = models.BooleanField(default=0)
    date = models.CharField(max_length=200, default='')

    def get_total_sum(self):
        return sum(item.get_sum() for item in self.orderid.all())

class MealToOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='meal', null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.meals_id.price * self.count


class Check(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order', null=True)
    servicefee = models.ForeignKey(ServicePercentage, on_delete=models.CASCADE, related_name='servicefee', null=True)
    date = models.CharField(max_length=100, default='')

    def get_total(self):
        return self.orderid.get_total_sum() * (1 + (self.servicefee.percentage / 100))
