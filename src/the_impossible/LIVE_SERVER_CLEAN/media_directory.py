# Delete folders that doesn't contain any files
# (Invisible files are ignored)

import os, shutil

ROOT = '/home/micha31r/webapps/theimpossible_media'

def main(directory):
	content = os.listdir(directory)
	for item in content:
		if len(item.split(".")) == 1:
			main(f"{directory}/{item}")

		# Remove invisible files
		if item[0] == ".":
			os.remove(f"{directory}/{item}")

	content = os.listdir(directory)
	# Delete the current folder if no it has no children
	if not content:
		if directory != ROOT:
			shutil.rmtree(directory)

main(ROOT)