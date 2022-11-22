from django.db import models
from django.urls import reverse


# class Publication(models.Model):
#     title = models.CharField(max_length=30)

#     class Meta:
#         ordering = ['title']

#     def __str__(self):
#         return self.title

# class Article(models.Model):
#     headline = models.CharField(max_length=100)
#     publications = models.ManyToManyField(Publication)

#     class Meta:
#         ordering = [  'headline']

#     def __str__(self):
#         return self.headline

# Create your models here.
class tadbirModel(models.Model):
    nametadbir = models.CharField(max_length=100)
    authuser = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    closeEvent = models.BooleanField(default=False)  # ombordami yuqmi

    def __str__(self):
        return self.nametadbir

    def get_absolute_url(self):
        return reverse('evensts', args=[str(self.id)])


class ratsiyaModel(models.Model):
    tadbir = models.ManyToManyField(tadbirModel, through='Enrollment')
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
    tadbirModel = models.ForeignKey(tadbirModel, on_delete=models.CASCADE)
    ratsiyaModel = models.ForeignKey(ratsiyaModel, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)

    #    final_grade = models.CharField(max_length=1, blank=True, null=True)
    class Meta:
        unique_together = [['tadbirModel', 'ratsiyaModel']]
