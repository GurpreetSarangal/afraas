from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, is_staff=False, **extra_fields):
        if not email:
            ValueError("email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff = is_staff,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password, **extra_fields):
        return self.create_user(email, password, is_staff=True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("super user must have is_staff True"))
        
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    # objects = UserManager()
