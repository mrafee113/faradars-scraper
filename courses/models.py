from django.db import models


class Tutor(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField()


class Course(models.Model):
    provider = models.CharField(max_length=100, choices=[('faradars',) * 2])
    title = models.TextField()
    link = models.URLField()
    number_of_students = models.IntegerField(default=-1)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    duration = models.DurationField(null=True)
