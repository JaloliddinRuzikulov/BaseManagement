from atexit import register
from django.contrib import admin
from .models import RatsiyaModel,TadbirModel,Enrollment
# Register your models here.
admin.site.register(RatsiyaModel)
admin.site.register(TadbirModel)
admin.site.register(Enrollment)
