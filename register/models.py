from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxLengthValidator

from rest_framework_simplejwt.tokens import RefreshToken

from register.managers import CustomUserManager
from common.models import BaseModel


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    date_joined = models.DateField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def hashing_password(self):
        self.set_password(self.password) if not self.password.startswith('pbkdf2_sha256') else False

    # def check_is_admin(self):
    #     self.is_staff = True if self.is_admin else False

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def save(self, *args, **kwargs):
        self.hashing_password()
        # self.check_is_admin()
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'user'


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    social_network = models.ForeignKey('SocialNetwork', on_delete=models.CASCADE,
                                       related_name='profiles', blank=True, null=True)

    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    small_description = models.TextField(validators=[MaxLengthValidator(limit_value=70)], blank=True, null=True)
    big_description = models.TextField(validators=[MaxLengthValidator(limit_value=200)], blank=True, null=True)
    email = models.EmailField()
    job_title = models.CharField(max_length=50, default='Jurnalist')
    date_of_brith = models.DateField(blank=True, null=True, default='2000-01-01')

    def __str__(self):
        return self.user.name

    def check_email(self):
        self.email = self.user.email if not self.email else None

    def check_full_name(self):
        self.full_name = self.user.name if not self.full_name else None

    def save(self, *args, **kwargs):
        self.clean()
        super(Profile, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_full_name()

    class Meta:
        db_table = 'profile'


class SocialNetwork(BaseModel):
    title = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'socialnetwork'


class VerificationCode(BaseModel):
    class VerifyType(models.TextChoices):
        TO_CONFIRM = 'to_confirm', 'to_confirm'
        TO_AUTH = 'to_register', 'to_register'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')

    code = models.CharField(max_length=5)
    verify_type = models.CharField(max_length=11, choices=VerifyType.choices)
    expiration_time = models.DateTimeField
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if self.code:
            self.expiration_time = datetime.now() + timedelta(minutes=2)
        else:
            pass
        super(VerificationCode, self).save(*args, **kwargs)
