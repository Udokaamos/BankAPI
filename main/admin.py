from django.contrib import admin
from django.contrib.auth import get_user_model
# from .models import User

# from .models import User
# from main.models import Bank

# Register your models here.
User = get_user_model()
admin.site.register(User)