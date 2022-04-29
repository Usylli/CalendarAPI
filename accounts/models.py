from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, name, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email_adress = self.normalize_email(email),
            name = name,
            username = username,
            **other_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
    def create_superuser(self, email, username, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Please assign is_staff=True for superuser')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Please assign is_superuser=True for superuser')
        
        return self.create_user(email, username, name, password, **other_fields)

class Users(AbstractBaseUser):
    email_address = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, default=None)
    name = models.CharField(max_length=30, blank=True, null=True, default=None)
    username = models.CharField(max_length=30, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email_address'
    
    objects=CustomAccountManager()
    
    class Meta:
        db_table = "tbl_users"
        
    def __str__(self):
        return str(self.email_address)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser


