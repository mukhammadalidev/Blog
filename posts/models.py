from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount
from users.models import CustomerUser

class Author(models.Model):
    author = models.ForeignKey(CustomerUser, on_delete=models.CASCADE,related_name='users')



    def __str__(self):
        return self.author.username

DR = 'draft'
PB = 'published'


class Like(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(HitCountMixin,models.Model):
    slug = models.SlugField(max_length=200)
    title = models.CharField(max_length=150)
    description = models.TextField()
    post_picture = models.ImageField(default='',upload_to='media/')
    author =models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(CustomerUser,through=Like,related_name='post_like')


    STATUS_CHOICES = (
        (DR,DR),
        (PB,PB)
    )
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default=DR)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering =['-created_time']






class PostAuthor(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    posts = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.author.author.username



class PostReview(models.Model):
    author = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.TextField()
    review = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_time']

    