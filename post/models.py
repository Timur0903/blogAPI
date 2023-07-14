from django.db import models

from category.models import Category


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255,unique=True)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='posts')
    preview = models.ImageField(upload_to='images/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} -- {self.title[:50]}'

    class Meta:
        ordering = ['created_at']

class PostImages(models.Model):
    title = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='image/')
    post = models.ForeignKey(Post,related_name = 'images',on_delete=models.CASCADE)


    def generate_name(self):
        from random import randint
        return 'image' + str(self.id) + str(randint(100000,1_000_000))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return  super(PostImages,self).save(*args,**kwargs)
