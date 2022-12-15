from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    #! identify the object the tag is applied to:
    # product = models.ForeignKey(Product) -> This is not a good way to implement this
    # as u r dependent on Product

    # ?Second Approach:
    # *type of object -> eg.product, video, blog..
    # *ID
    # as using the type we can find the table, and using the ID we can find the record
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey()
    # we can read the actual object by this
