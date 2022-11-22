from atexit import register
from django.contrib import admin
from .models import ratsiyaModel,tadbirModel,Enrollment
# Register your models here.
admin.site.register(ratsiyaModel)
admin.site.register(tadbirModel)
admin.site.register(Enrollment)
