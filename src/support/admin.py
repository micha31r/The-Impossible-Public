from django.contrib import admin
from .models import (
	Feedback,
	Question,
	CoreFeed
)

class FeedbackAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('__str__','author','viewed','id','timestamp')
    search_fields = ('author__user__username',)
    readonly_fields = ["timestamp"]

class QuestionAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('author','short_description','solved','id','timestamp')
    search_fields = ('author__user__username',)
    readonly_fields = ["timestamp"]

class CoreFeedAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('name','publish_status','id','timestamp')
    search_fields = ('name','publish_status')
    readonly_fields = ["timestamp"]

admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(CoreFeed,CoreFeedAdmin)