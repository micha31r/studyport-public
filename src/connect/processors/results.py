import uuid, base64, logging
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware
from results.models import Result
from results.conversion import name_to_abbv
from group.models import School
from standards.models import Assessment, Subject
from usermgmt.models import Student
import logging

logger = logging.getLogger(__name__)

# https://directoryservices.kamar.nz/?listening-service/Messages/assessments

def run(data):
	success = True
	results = data["results"]["data"]

	for i in range(len(results)-1, -1, -1):
		item = results[i]

		if item["type"] in ["A", "U", "G"]:
			id_ 		= item["id"]
			number 		= item["number"]
			subject 	= item["subject"]
			result 		= item["result"]
			type_ 		= item["type"]
			date 		= item["date"]
			yearlevel 	= item["yearlevel"]
			published 	= item["published"]

			if not (id_ and number and subject and date and yearlevel):
				success = False
				continue

			try: 
				student = Student.objects.get(student_id=id_, school__moe_code=data["schools"][0]["moeCode"])
				assessment = Assessment.objects.get(assessment_code=number)
				subject = Subject.objects.get(subject_code=subject)
				if settings.DEBUG:
					date = make_aware(datetime.strptime(date, "%Y%m%d"))
				else:
					# Use the sync time as date in production
					date = timezone.now().date()
			except Exception as e:
				if settings.DEBUG: print(e)
				success = False
				continue

			obj = Result.objects.filter(student=student, assessment=assessment).first()
			if not obj:
				obj = Result.objects.create(
					student 		= student,
					subject 		= subject,
					assessment 		= assessment,
					grade 			= name_to_abbv(result),
					# is_published 	= published,
					date 			= date,
					is_mock			= (type_ == "G")
				)
			else:
				obj.student 		= student
				obj.subject 		= subject
				obj.assessment 		= assessment
				obj.grade 			= name_to_abbv(result)
				# obj.is_published 	= published
				obj.date 			= date
				obj.is_mock = (type_ == "G")
				obj.save()

			results.pop(i)

	data["results"]["count"] = len(results)
	data["results"]["data"] = results
	return success, data["results"]