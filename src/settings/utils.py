import os, glob
from django.conf import settings

def get_profile_image_names(choice_format=False):
	files = glob.glob(os.path.join(settings.BASE_DIR, "project/static/icons8/profile/*"))
	names = []
	for path in files:
		name = "".join(path.split("/")[-1].split(".")[:-1])
		if choice_format:
			names.append((name, name))
		else:
			names.append(name)
	return names
