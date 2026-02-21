from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):

    phone = models.CharField(max_length=15, unique=True)



class UserProfile(models.Model):

    height = models.FloatField()

    weight = models.FloatField()

    age = models.PositiveIntegerField()

    GENDER_OPTIONS=(
        ("male","male"),
        ("female","female")
    )

    gender = models.CharField(max_length=200,choices=GENDER_OPTIONS,default="male")


    ACTIVITY_CHOICES=(
        ("1.2","Sedentary (little/no exercise)"),
        ("1.375","Lightly active (exercise 1-3 days/week)"),
        ("1.55","Moderately active (exercise 3-5 days/week)"),
        ("1.725","Very active (exercise 6-7 days/week)"),
        ("1.9","Extra active (very intense activity)")
    )


    activity_level = models.CharField(max_length=200,choices=ACTIVITY_CHOICES,default="1.2")

    bmr = models.FloatField(null=True)

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")