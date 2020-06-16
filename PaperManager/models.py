from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Space(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    filesize = models.IntegerField(verbose_name="File Size (MB)")

    def __str__(self):
        return self.user.username


class Paper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, verbose_name="Title")
    author = models.CharField(max_length=512)
    filename = models.FilePathField(recursive=True)
    filebin = models.FileField(upload_to=user_directory_path)
    filesize = models.FloatField(verbose_name="File Size (MB)")

    def __str__(self):
        return self.name
