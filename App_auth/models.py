from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy


# Create your models here.
class MainManager(BaseUserManager):
    """ A custom Manager to deal with emails as unique identifer """

    def _create_user(self, email, password, **extra_fields):
        """ Creates and saves a user with a given email and password"""

        if not email:
            raise ValueError("The Email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False,
        help_text=gettext_lazy('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True,
        help_text=gettext_lazy(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'
    objects = MainManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$", message=gettext_lazy(
    "Enter a valid international mobile phone number starting with +(country code)"))
gender_choice = (
    ("male", "Male"),
    ("Female", "Female"),
    ("Third Gender", "Third Gender")
)


# Create your models here.
class EmployeeProfileModel(models.Model):
    employee_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='employee_user')
    employee_picture = models.ImageField(upload_to='EmployeeProfileModel/employee_photo')
    fullName = models.CharField(max_length=100)
    employee_contact = models.CharField(validators=[phone_regex], verbose_name=gettext_lazy("Employee's Mobile phone"),
                                        max_length=17, blank=True, null=True)
    Date_of_Birth = models.DateField(blank=False)
    gender = models.CharField(choices=gender_choice, max_length=15)
    employee_nid = models.IntegerField(unique=False)
    employee_address = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=50, unique=True)
    employee_designation = models.CharField(max_length=100)
    employee_salary = models.IntegerField(unique=False)
    joining_date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.employee_id}-{self.fullName} {self.employee_designation}"


Department = (
    ('Accounts', 'Accounts'),
)


class BossModel(models.Model):
    boss_picture = models.ImageField(upload_to='BossProfileModel/boss_photo')
    fullName = models.CharField(max_length=100)
    boss_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='boss_user')
    boss_contact = models.CharField(validators=[phone_regex], verbose_name=gettext_lazy("Employee's Mobile phone"),
                                    max_length=17, blank=True, null=True)
    Date_of_Birth = models.DateField(blank=False)
    gender = models.CharField(choices=gender_choice, max_length=15)
    boss_nid = models.IntegerField(unique=False)
    boss_address = models.CharField(max_length=200)
    boss_id = models.CharField(max_length=50, unique=True)
    boss_designation = models.CharField(max_length=100)
    boss_salary = models.IntegerField(unique=False)
    joining_date = models.DateField(blank=False)
    head_of_dpt = models.CharField(max_length=200, choices=Department)

    def __str__(self):
        return f"{self.fullName} {self.head_of_dpt}"
