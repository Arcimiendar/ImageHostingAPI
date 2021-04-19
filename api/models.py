from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.storage import get_storage_class
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator

from thumbnails.fields import ImageField
from PIL import Image as ImageObject

from io import BytesIO
from datetime import timedelta

import os


User = get_user_model()
Storage = get_storage_class()


class Image(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = ImageField()

    def save(self, *args, **kwargs):
        status = super(Image, self).save(*args, **kwargs)
        if not hasattr(self.uploader, 'account_plan_assignement'):
            assignement = AccountPlanAssignement.objects.create(user=self.uploader, account_plan_id=1)
            sizes = assignement.account_plan.thumbnail_sizes.filter(~models.Q(thumbnail__in=self.thumbnails.all()))
        else:
            sizes = self.uploader.account_plan_assignement.account_plan.thumbnail_sizes.filter(
               ~models.Q(thumbnail__in=self.thumbnails.all())
            )
        storage = Storage()
        for size in sizes:
            img = ImageObject.open(self.image_file.file.file)
            img.thumbnail((size.width, size.height))
            new_img_io = BytesIO()
            img.save(new_img_io, format='JPEG')
            splitted_ext = os.path.splitext(self.image_file.path)
            if len(splitted_ext) > 1:
                filename, ext = splitted_ext
            else:
                filename, ext = splitted_ext[0], '.jpg'
            filename = storage.generate_filename(filename + str(size) + ext)
            storage.save(filename, new_img_io)

            Thumbnail.objects.create(
                thumbnail_size=size, original_image=self,
                thumbnail_image=storage.open(filename)
            )

        return status


class ThumbnailSize(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    class Meta:
        unique_together = ('width', 'height')

    def __str__(self):
        return f'size {self.width}x{self.height}'


class Thumbnail(models.Model):
    thumbnail_size = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE)
    original_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='thumbnails')
    thumbnail_image = ImageField()

    class Meta:
        unique_together = ('thumbnail_size', 'original_image')


class AccountPlan(models.Model):
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, related_name='account_plans')
    have_access_to_original_link = models.BooleanField(default=False)
    can_create_expirable_links = models.BooleanField(default=False)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'


class AccountPlanAssignement(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='account_plan_assignement'
    )
    account_plan = models.ForeignKey(AccountPlan, on_delete=models.SET_DEFAULT, null=True, default=1)

    def __str__(self):
        return f'{self.account_plan} to {self.user}'


class ExpirableLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=now)
    experation_period = models.DurationField(validators=[
        MinValueValidator(timedelta(seconds=300)),
        MaxValueValidator(timedelta(seconds=30000))
    ])

    @classmethod
    def filter_by_temporary_link(cls, temporary_link):
        return cls.objects.filter(pk=int(temporary_link))

    def generate_temporary_link(self, request=None):
        obj = reverse('temporary-link', kwargs={'expirable_link': self.id})
        if request:
            return request.build_absolute_uri(obj)
        else:
            return obj

    def __str__(self):
        return f'Expirable  link {self.image} created_at {self.time_created} experation_period {self.experation_period}'
