from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import os

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def validate_image(image):
    megabyte_limit = 2
    if image.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальний розмір зображення — {megabyte_limit}MB")

    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Дозволені формати: JPEG або PNG")

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    image = CloudinaryField(
    'image',
    null=True,
    blank=True
    )



    def __str__(self):
        return self.title

    def vote_score(self):
        return self.votes.aggregate(score=models.Sum('value'))['score'] or 0

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Коментар:')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коментар від {self.author} на {self.post}'
