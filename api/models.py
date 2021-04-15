from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from thumbnails.fields import ImageField

from datetime import timedelta


User = get_user_model()


class Image(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = ImageField()


class ThumbnailSize(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    class Meta:
        unique_together = ('width', 'height')

    def __str__(self):
        return f'size {self.width}x{self.height}'


class AccountPlan(models.Model):
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, related_name='account_plans')
    have_access_to_original_link = models.BooleanField(default=bool)  # default False
    can_create_expirable_links = models.BooleanField(default=bool)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'


class AccountPlanAssignement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account = models.ForeignKey(AccountPlan, on_delete=models.SET_DEFAULT, null=True, default=1)

    def __str__(self):
        return f'{self.account} to {self.user}'


class ExpirableLink(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=now)
    experation_period = models.DurationField(validators=[
        MinValueValidator(timedelta(seconds=300)),
        MaxValueValidator(timedelta(seconds=30000))
    ])
