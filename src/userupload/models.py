import string, random, os
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL

from the_impossible.utils import *

SUPPORTED_FILE_TYPE = {
	"video":[
		"mp4",
		"mov",
		"webm"
	],
	"image":[
		"png",
		"jpg",
		"JPG",
		"jpeg",
		"JPEG",
		"gif",
		"svg"
	],
	"other":[ 
		"zip",
		"pdf",
	]
}

def slug_generator(seed,size=20, chars=string.ascii_letters + string.digits):
	random.seed(seed)
	return ''.join(random.choice(chars) for _ in range(size))

def user_directory_path(instance,filename):
	date = Date()
	slug = slug_generator(instance.user.id,size=40)
	extension = filename.split(".")[-1] 
	name = filename.replace(f".{extension}","") + "__" + slug
	return f'uploaded/userid_{instance.user.id}/{extension}/{date.year()}/{date.month()}/{date.day()}/{name}.{extension}'

def validate_file_size(value):
    size = value.size
    if size > 10485760: raise ValidationError("Maximum file size allowed is 10MB")
    else: return value

class File(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
	description = models.CharField(max_length=100)
	file = models.FileField(upload_to=user_directory_path,validators=[validate_file_size])
	# Timestamp
	timestamp = models.DateTimeField(auto_now_add=True) 
	last_edit = models.DateTimeField(auto_now=True)

	def delete(self, *args, **kwargs):
		# Delete uploaded file
		if os.path.isfile(self.file.path):
			os.remove(self.file.path)

		super(File,self).delete(*args,**kwargs)

	def __str__(self):
		name = self.file.name.split("/")[-1].split(".")[0]
		if len(name) > 20:
			name = name[:20] + "..."
		return name

