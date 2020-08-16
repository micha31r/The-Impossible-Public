from django.contrib import admin
from .models import (
	Tag,
	Idea,
    Comment
)

# https://stackoverflow.com/questions/48372252/django-admin-accessing-reverse-many-to-many
class IdeaInline(admin.TabularInline):
	model = Idea.tags.through


class TagAdmin(admin.ModelAdmin):
	inlines = [IdeaInline]


class IdeaAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('name','author','view_count','like_count','comment_count','id','last_edit','timestamp')
        
    search_fields = ('name','author__user__username')

    def view_count(self,obj):
        return obj.viewed_user.all().count()

    def like_count(self,obj):
        return obj.liked_user.all().count()

    def comment_count(self,obj):
        return obj.comments.all().count()

    readonly_fields = ["timestamp"]

class CommentAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('__str__','author','id','last_edit','timestamp')
    search_fields = ('author__user__username',)
    readonly_fields = ["timestamp"]

admin.site.register(Tag,TagAdmin)
admin.site.register(Idea,IdeaAdmin)
admin.site.register(Comment,CommentAdmin)
