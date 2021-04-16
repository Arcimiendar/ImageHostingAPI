from django.contrib import admin
from api.models import Image, ThumbnailSize, ExpirableLink, AccountPlan, AccountPlanAssignement, Thumbnail


admin.site.register(Image)
admin.site.register(ThumbnailSize)
admin.site.register(ExpirableLink)
admin.site.register(AccountPlan)
admin.site.register(AccountPlanAssignement)
admin.site.register(Thumbnail)

