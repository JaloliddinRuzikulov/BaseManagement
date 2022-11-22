from django.db import models
from django.urls import reverse


class TadbirModel(models.Model):
    nametadbir = models.CharField(max_length=100)
    authuser = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    closeEvent = models.BooleanField(default=False)  # ombordami yuqmi
    def __str__(self):
        return self.nametadbir

    def get_absolute_url(self):
        return reverse('evensts', args=[str(self.id)])


class RatsiyaModel(models.Model):
    tadbir = models.ManyToManyField(TadbirModel, through='Enrollment')
    katalog = models.CharField(max_length=200)
    rcode = models.SmallIntegerField(default=0)
    model = models.CharField(max_length=200)
    qr_code = models.CharField(max_length=200)
    lasteventid = models.PositiveIntegerField(default=0)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('detial', args=[str(self.pk)])


class Enrollment(models.Model):
    TadbirModel = models.ForeignKey(TadbirModel, on_delete=models.CASCADE)
    RatsiyaModel = models.ForeignKey(RatsiyaModel, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)

    class Meta:
        unique_together = [['TadbirModel', 'RatsiyaModel']]
