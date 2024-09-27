from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django.utils.text import slugify


from django_ckeditor_5.fields import CKEditor5Field


class ArticleContent(models.Model):
    title=models.CharField('Title', max_length=200)
    text=CKEditor5Field('Text', config_name='extends')

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class Article(models.Model):
    """
    A model to create and manage articles
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="article_posts")
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    content = CKEditor5Field(max_length=5000, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(
        max_length=100, default='default alt', null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    excerpt = models.TextField(max_length=300, null=False, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    # A boolean flag for soft deletion. When True, the article is considered deleted,
    # but the record is still kept in the database. Default is False (not deleted).
    is_deleted = models.BooleanField(default=False)

    class Meta:
        """ Order articles by posted date date """
        ordering = ["-posted_date"]

    def save(self, *args, **kwargs):
        # Generate the slug if it's not already set
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Article, self).save(*args, **kwargs)