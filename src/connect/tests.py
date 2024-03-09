import sys, requests, json, demjson3, os, glob
from django.conf import settings


def push(name="*"):
	# Basic authentication
	headers = {
		"Authorization": "",
	}

	filename = name + ".json"

	paths = glob.glob(os.path.join(settings.BASE_DIR, "connect", "test_data", filename))
	for path in paths:
		with open(path, 'r') as f:
			data = demjson3.decode(f.read())

		url = 'https://connect.studyport.co'
		if settings.DEBUG:
			url = 'http://connect.localhost:8000'
		response = requests.post(url, json=data, headers=headers)

		# Format request headers
		cleaned = {}
		for k, v in response.headers.items():
			cleaned[k] = str(v)

		print(response)
		# print(json.dumps(cleaned, indent=4))
		print(response.text)


push()


def generate_subject_json_from_list():
	raw = input("Paste subject names (seperated by comma [,])")
	data = []
	for i in range(3):
		for name in raw.split(","):
			subject_code = "".join(c for c in name if c.isalnum()) # Remove all non-alphanumeric characters
			subject_code = "".join(x[0] for x in name.split(" ")) # Get initials
			# If initials is shorter than 3 characters then get the first three characters of the subject name
			if len(subject_code) < 3:
				subject_code = name[:3]
			data.append({
				"id": subject_code.upper() + str(i + 1), 
				"name": name, 
				"department": "Lorem Ipsum", 
				"qualification": "l" + str(i + 1), 
				"level": 11 + i, 
			})
	print(json.dumps(data, indent=4))









