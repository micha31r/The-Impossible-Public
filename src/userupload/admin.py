from django.contrib import admin
from .models import File

import os

class FileAdmin(admin.ModelAdmin):
	# Display custom fields in Django admin
	list_display = ("file_name","file_extension","file_size","user","id","timestamp","last_edit")

	search_fields = ('id',)

	def file_name(self,obj):
		name = obj.file.name.split("/")[-1].split(".")[0]
		if len(name) > 20:
			name = name[:20] + "..."
		return name

	def file_extension(self,obj):
		extension = obj.file.name.split("/")[-1].split(".")[-1]
		return extension

	def file_size(self,obj):
		fullpath = obj.file.path
		size = os.path.getsize(fullpath)
		size = round(int(size)/1024/1024,2)
		return f"{str(size)} MB"

	readonly_fields = ["timestamp"]


admin.site.register(File,FileAdmin)