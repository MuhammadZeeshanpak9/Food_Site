from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
## !IMPORTANT
 ##Every Time When You Make your own model go to settings.py and Merge this file in Settings.py Like "AUTH_USER_MODEL='YOUR APP nAME.USER"


# managers.py (or wherever you defined it)
class UserManager(BaseUserManager):
    def create_user(self, Email, Name, Gender, password=None):
        """
        Creates and saves a User with the given Email, Name, Gender, and password.
        """
        if not Email:
            raise ValueError("Users must have an email address")

        user = self.model(
            Email=self.normalize_email(Email),
            Name=Name,
            Gender=Gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, Name, Gender, password=None):
        """
        Creates and saves a superuser with the given Email, Name, Gender, and password.
        """
        user = self.create_user(
            Email=self.normalize_email(Email),
            Name=Name,
            Gender=Gender,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



# models.py
class User(AbstractBaseUser):
    Email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = ["Name", "Gender"]

    def __str__(self):
        return self.Email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
