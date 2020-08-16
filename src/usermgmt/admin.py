from django.contrib import admin
from .models import (
	Notification,
	Profile,
    Verification
)

class NotificationAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('__str__','message_status','dismissed','id','timestamp')
    search_fields = ('message_status','dismissed')
    readonly_fields = ["timestamp"]

class ProfileAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('user','timestamp','daily_limit','daily_limit_timestamp')
    search_fields = ('user__username',)
    readonly_fields = ["timestamp"]

class VerificationAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ('user','slug')
    search_fields = ('user__username',)

admin.site.register(Notification,NotificationAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Verification,VerificationAdmin)
