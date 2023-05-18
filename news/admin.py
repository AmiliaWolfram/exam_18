from django.contrib import admin

from .models import Status, CommentStatus, NewsStatus

admin.site.register(Status)
admin.site.register(CommentStatus)
admin.site.register(NewsStatus)
