from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

"""
As with ForeignKey fields, the related_name attribute of ManyToManyField
allows you to name the relationship from the related object back to this one. The
ManyToManyField fields provide a many-to-many manager that allows you to
retrieve related objects, such as image.users_like.all(), or get them from
a user object, such as user.images_liked.all().
"""
class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])