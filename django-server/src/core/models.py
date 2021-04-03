from datetime import datetime
from djongo import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify


class Base(models.Model):
    """
    This is the abstract base model to be inherited by all other models.
    """
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    is_deleted = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False, db_index=True)

    objects = models.DjongoManager()

    class Meta:
        abstract = True
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # update the 'updated_at' field if the record already exists
        if self.id is not None:
            self.updated_at = datetime.now()

        super().save(*args, **kwargs)


class InfoMeta(models.Model):
    """
    This abstract model provides a title and description field.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class Slugged(models.Model):
    """
    This abstract model is inherited by all other models which need a unique
    slug based on the name.
    """
    name = models.CharField(max_length=250)
    slug = models.CharField(unique=True, blank=True, max_length=255)

    objects = models.DjongoManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()

        super().save(*args, **kwargs)

    def get_unique_slug(self):
        """
        Generates a unique slug from the name.

        Returns:
            str: The final unique slug.
        """
        max_slug_length = self.__class__._meta.get_field('slug').max_length
        generated_slug = slugify(
                self.name, allow_unicode=True)[:max_slug_length]
        similar_slugs = self.__class__.objects.filter(
                slug__istartswith=generated_slug).values_list(
                        'slug', flat=True)
        if similar_slugs:
            slug_counter = 1
            while generated_slug in similar_slugs:
                generated_slug = '{}-{}'.format(generated_slug, slug_counter)
                slug_counter += 1

        return generated_slug


class ModelHistory(models.Model):
    """
    This model stores the change history for all models in JSON format.
    """
    created_at = models.DateTimeField(default=datetime.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    data = models.TextField()

    objects = models.DjongoManager()

    def __str__(self):
        return '{} - {}'.format(self.content_type.name, self.content_object)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Model History'
        verbose_name_plural = 'Model History'
