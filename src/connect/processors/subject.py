import uuid, base64
from standards.models import Subject

# https://directoryservices.kamar.nz/?listening-service/Messages/subjects

def run(data):
	success = True
	subjects = data["subjects"]["data"]

	for i in range(len(subjects)-1, -1, -1):
		item = subjects[i]

		id_ 			= item["id"]
		name 			= item["name"]
		department 		= item["department"]
		qualification 	= item["qualification"]
		level 		    = item["level"]

		if not (id_ and name and department and qualification and level):
			success = False
			continue

		obj = Subject.objects.filter(subject_code=id_).first()
		if not obj:
			obj = Subject.objects.create(
				subject_code 	= id_,
				name 			= name,
				department 		= department,
				qualification 	= qualification,
				year_level 		= level,
			)
		else:
			obj.subject_code 	= id_
			obj.name 			= name
			obj.department 		= department
			obj.qualification 	= qualification
			obj.year_level 		= level
			obj.save()

		subjects.pop(i)

	data["subjects"]["count"] = len(subjects)
	data["subjects"]["data"] = subjects
	return success, data["subjects"]