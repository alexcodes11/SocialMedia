from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class User(AbstractUser):
    pass

class Posts(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=280)
    likes = models.ManyToManyField(User, related_name='post_like')
    timestamp = models.DateTimeField(auto_now_add=True)

    
class Following(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE, related_name="peron_following" )
    following = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return "who is %s following" % self.person.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     
        Following.objects.create(person=instance)


class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete= models.CASCADE , related_name='post_id')
    likes = models.ManyToManyField(User, related_name= 'likes')



