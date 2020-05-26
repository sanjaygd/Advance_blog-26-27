from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey # This is added in generic foriegnkey part-2
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse

from django.db import models

# Added in AD-14    
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager,self).filter(parent=None)
        return qs
    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager,self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()
    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse('comments:thread', kwargs={'id':self.id})

    def get_delete_url(self):
        return reverse('comments:comment_delete', kwargs={'id':self.id})

    def children(self):
        return Comments.objects.filter(parent = self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True



