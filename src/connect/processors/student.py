import base64
from django.conf import settings
from django.contrib.auth.models import User
from usermgmt.models import Student
from .utils import get_school

# https://directoryservices.kamar.nz/?listening-service/Messages/students-and-staff
# https://directoryservices.kamar.nz/?listening-service/check-fields

def run(data):
	success = True
	schools = data["schools"]
	students = data["students"]["data"]
	student_record = []

	for i in range(len(students)-1, -1, -1):
		item = students[i]

		id_ 			= item["id"]
		firstnamelegal 	= item["firstnamelegal"]
		lastnamelegal 	= item["lastnamelegal"]
		email 			= item["email"]
		yearlevel 		= item["yearlevel"]
		startingdate 	= item["startingdate"]
		schoolindex 	= item["schoolindex"]

		try: 
			startingdate = make_aware(datetime.strptime(startingdate, "%Y%m%d"))
		except Exception as e:
			if settings.DEBUG: print(e)
			success = False
			continue

		school = get_school(schools, schoolindex)
		if not school:
			success = False
			continue

		if not (id_ and firstnamelegal and lastnamelegal and email and yearlevel and startingdate and schoolindex):
			success = False
			continue

		user = User.objects.filter(username=email).first()
		if not user:
			user = User.objects.create(
				first_name 	= firstnamelegal,
				last_name 	= lastnamelegal,
				username 	= email,
				is_active 	= False,
			)

			profile = Student.objects.create(
				user 			= user,
				year_level 		= yearlevel,
				school 			= school,
				student_id 		= id_,
				starting_date 	= startingdate
			)
		else:
			profile = Student.objects.filter(user=user).first()
			if profile:
				profile.user.first_name = firstnamelegal
				profile.user.last_name 	= lastnamelegal
				profile.user.username 	= email
				profile.user.save()
				
				profile.year_level 		= yearlevel
				profile.school 			= school
				profile.student_id 		= id_
				profile.starting_date 	= startingdate
				profile.save()

		student_record.append(email)
		students.pop(i)

	# Mark students (not the user obj) as inactive if they are not part of the full sync
	if data["sync"] == "full":
		for obj in Student.objects.all():
			if obj.user.email not in student_record:
				obj.is_active = False
				obj.save()

	data["students"]["count"] = len(students)
	data["students"]["data"] = students
	return success, data["students"]

