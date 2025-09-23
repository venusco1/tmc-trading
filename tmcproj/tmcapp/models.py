
from django.contrib.auth.models import User
from django.db import models


class AllowCourse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course_allowed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - Course Allowed: {self.course_allowed}'


class Video(models.Model):
    title = models.CharField(max_length=100)


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  
    is_unlocked = models.BooleanField(default=False)
    watched_previous = models.BooleanField(default=False)

