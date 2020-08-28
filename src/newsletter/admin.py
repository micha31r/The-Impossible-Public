from django.contrib import admin

from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    # Display custom fields in Django admin
    list_display = ("email","slug","last_sent","id","timestamp")
    search_fields = ("email",)
    readonly_fields = ["timestamp"]

admin.site.register(Subscriber,SubscriberAdmin)
