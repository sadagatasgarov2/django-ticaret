import datetime
from builtins import bool, type
from pyexpat import model

from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, Select, ImageField, FileInput
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from django_extensions.db.fields import AutoSlugField

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(MPTTModel):
    STATUS = (
        ('True', True),
        ('False', False)
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    # context = models.OneToOneRel(Content, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::1])



TYPE = (
    ('menu', 'menu'),
    ('haber', 'haber'),
    ('duyuru', 'duyuru'),
    ('etkinlik', 'etkinlik'),
)

STATUS = (
    ('True', 'True'),
    ('False', 'False')
)

class Content(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu = models.OneToOneField(Menu, null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE)
    title = models.CharField(max_length=150)
    keyword = models.CharField(blank=True, max_length=255)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=False, upload_to='images/')
    detail = RichTextUploadingField()
    slug = AutoSlugField(populate_from=['title', 'date'])
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    date = datetime.datetime.now()

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('content_detail', kwargs={'slug': self.slug})

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['type', 'title', 'keyword', 'description', 'image', 'detail']
        widgets = {
            'type': Select(attrs={'class': 'input', 'placeholder': 'type'}, choices=TYPE),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keyword': TextInput(attrs={'class': 'input', 'placeholder': 'keyword'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'detail': RichTextUploadingField(),
            'status': 'False'
        }


class CImages(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=False, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'
