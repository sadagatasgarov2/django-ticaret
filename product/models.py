import datetime
from pyexpat import model

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(blank=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=False, upload_to='images/')
    price = models.FloatField()
    amount = models.PositiveIntegerField()
    minamount = models.IntegerField(default=0)
    detail = RichTextUploadingField()
    slug = AutoSlugField(populate_from=['title', 'date'])
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    date = datetime.datetime.now()

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    # method to create a fake table field in read only mode

    def catimg_tag(self):
        return mark_safe((Category.status))

    def sluqdt(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return ""
        else:
            return mark_safe('<img src="{}" height="50">'.format(self.image.url))

    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayir'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=250, blank=False)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
