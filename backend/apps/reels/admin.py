from django.contrib import admin
from .models import Reel, ReelComment, ReelLike, ReelCommentLike
# Register your models here.
admin.site.register(Reel)
admin.site.register(ReelComment)
admin.site.register(ReelLike)
admin.site.register(ReelCommentLike)