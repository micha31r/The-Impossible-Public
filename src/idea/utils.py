import re

def at_filter(data):
	usernames = []
	for word in data.split(" "):
		if "@" in word:
			usernames.append(word.split("@")[-1])
	return usernames

# Escape HTML codes
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def escape_html(raw_html):
	cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext