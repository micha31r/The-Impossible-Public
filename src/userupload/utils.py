from .models import SUPPORTED_FILE_TYPE, File

# get file extension
def file_extension(name):
	return (name.split(".")[-1]).lower()

def file_is_valid(name,expected_type):
	# Return file type
	extension = file_extension(name)
	if expected_type in SUPPORTED_FILE_TYPE.keys():
		for v in SUPPORTED_FILE_TYPE[expected_type]:
			if extension == v:
				return True
	return False