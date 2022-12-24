from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required.")
        if not username:
            raise ValueError("Username is required.")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_filepath(self, filename):
    return f"profile_images/{self.pk}/profile.png"


def get_banner_filepath(self, filename):
    return f"banner_images/{self.pk}/banner.png"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    mobile = PhoneNumberField(blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to=get_profile_filepath, null=True, blank=True
    )
    banner_image = models.ImageField(
        upload_to=get_banner_filepath, null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_admin

    def has_module_perms(self, app_lable) -> bool:
        return True

    def is_staff_user(self) -> bool:
        return self.is_staff

    def is_superuser_user(self) -> bool:
        return self.is_superuser

    def is_staff_or_manager_user(self) -> bool:
        return self.is_staff or self.is_manager

    def get_full_name(self) -> str:
        return self.first_name + " " + self.last_name
