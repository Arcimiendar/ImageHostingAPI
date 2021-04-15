from django.contrib import admin
from api.models import Image, ThumbnailSize, ExpirableLink, AccountPlan

# Register your models here.
admin.site.register(Image)
admin.site.register(ThumbnailSize)
admin.site.register(ExpirableLink)
admin.site.register(AccountPlan)
